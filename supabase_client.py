"""
beautyflix/supabase_client.py
Substitua SUPABASE_URL e SUPABASE_KEY pelas suas credenciais do projeto gratuito.
No Colab: use userdata.get() ou os.environ para não expor as chaves.
"""

import os
from supabase import create_client, Client
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

_client: Client | None = None

def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ---- SUBSCRIBERS ----

def get_subscriber(email: str):
    db = get_client()
    res = db.table("subscribers").select("*").eq("email", email).single().execute()
    return res.data

def update_plan(subscriber_id: str, new_plan: str):
    db = get_client()
    db.table("subscribers").update({"plan": new_plan}).eq("id", subscriber_id).execute()


# ---- SALONS ----

def get_active_salons(city: str = "Joinville"):
    db = get_client()
    res = db.table("salons").select("*, salon_services(*)").eq("city", city).eq("status", "active").execute()
    return res.data

def get_salon_services(salon_id: str):
    db = get_client()
    res = db.table("salon_services").select("*").eq("salon_id", salon_id).eq("active", True).execute()
    return res.data


# ---- SLOTS ----

def get_available_slots(salon_id: str, slot_date: str):
    db = get_client()
    res = (db.table("available_slots")
             .select("*")
             .eq("salon_id", salon_id)
             .eq("slot_date", slot_date)
             .eq("is_booked", False)
             .order("slot_time")
             .execute())
    return res.data

def upsert_slots(salon_id: str, slot_date: str, times: list[str]):
    db = get_client()
    rows = [{"salon_id": salon_id, "slot_date": slot_date, "slot_time": t} for t in times]
    db.table("available_slots").upsert(rows, on_conflict="salon_id,slot_date,slot_time").execute()


# ---- BOOKINGS ----

def create_booking(subscriber_id: str, salon_id: str, slot_id: str,
                   procedure: str, booking_date: str, booking_time: str, value: float):
    db = get_client()
    # Cria o agendamento
    res = db.table("bookings").insert({
        "subscriber_id": subscriber_id,
        "salon_id": salon_id,
        "slot_id": slot_id,
        "procedure_name": procedure,
        "booking_date": booking_date,
        "booking_time": booking_time,
        "status": "confirmed",
        "platform_value": value,
    }).execute()
    # Marca o slot como ocupado
    db.table("available_slots").update({"is_booked": True}).eq("id", slot_id).execute()
    # Incrementa contador de uso da assinante
    db.rpc("increment_procedures_used", {"sub_id": subscriber_id}).execute()
    return res.data

def get_subscriber_bookings(subscriber_id: str):
    db = get_client()
    res = (db.table("bookings")
             .select("*, salons(name, address)")
             .eq("subscriber_id", subscriber_id)
             .order("booking_date", desc=True)
             .execute())
    return res.data

def get_salon_bookings(salon_id: str):
    db = get_client()
    res = (db.table("bookings")
             .select("*, subscribers(name, phone)")
             .eq("salon_id", salon_id)
             .in_("status", ["pending", "confirmed"])
             .order("booking_date")
             .execute())
    return res.data

def complete_booking(booking_id: str):
    db = get_client()
    db.table("bookings").update({"status": "completed"}).eq("id", booking_id).execute()


# ---- FINANCEIRO ----

def get_salon_balance(salon_id: str):
    db = get_client()
    res = (db.table("salon_payments")
             .select("amount")
             .eq("salon_id", salon_id)
             .eq("status", "pending")
             .execute())
    total = sum(r["amount"] for r in res.data) if res.data else 0.0
    return total
