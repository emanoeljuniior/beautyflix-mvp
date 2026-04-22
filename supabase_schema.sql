-- =============================================
-- BEAUTYFLIX MVP — Supabase Schema
-- =============================================

-- ASSINANTES
create table subscribers (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  email text unique not null,
  phone text,
  plan text check (plan in ('Starter','Plus','Premium')) default 'Starter',
  status text check (status in ('active','inactive','trial')) default 'active',
  procedures_used int default 0,
  member_since date default current_date,
  next_billing date,
  created_at timestamptz default now()
);

-- PLANOS
create table plans (
  id text primary key,
  name text not null,
  price numeric(10,2) not null,
  procedures_per_month int not null,
  features jsonb
);

insert into plans values
  ('starter', 'Starter', 79.90, 4, '["4 procedimentos/mês","Acesso a todos os salões","Agendamento pelo app"]'),
  ('plus',    'Plus',    139.90, 8, '["8 procedimentos/mês","Prioridade no agendamento","Suporte prioritário"]'),
  ('premium', 'Premium', 199.90, 14,'["14 procedimentos/mês","Consultor pessoal","Descontos especiais"]');

-- SALÕES PARCEIROS
create table salons (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  email text unique not null,
  phone text,
  address text,
  city text default 'Joinville',
  state text default 'SC',
  lat numeric(9,6),
  lng numeric(9,6),
  rating numeric(3,1) default 5.0,
  status text check (status in ('active','pending','suspended')) default 'pending',
  min_daily_slots int default 2,
  created_at timestamptz default now()
);

-- PROCEDIMENTOS OFERECIDOS POR CADA SALÃO
create table salon_services (
  id uuid default gen_random_uuid() primary key,
  salon_id uuid references salons(id) on delete cascade,
  procedure_name text not null,
  platform_price numeric(10,2) not null,  -- valor que o salão recebe
  full_price numeric(10,2),               -- valor de balcão (referência)
  active boolean default true,
  unique(salon_id, procedure_name)
);

-- HORÁRIOS DISPONÍVEIS (agenda do salão)
create table available_slots (
  id uuid default gen_random_uuid() primary key,
  salon_id uuid references salons(id) on delete cascade,
  slot_date date not null,
  slot_time time not null,
  procedure_name text,                    -- null = qualquer procedimento
  is_booked boolean default false,
  created_at timestamptz default now(),
  unique(salon_id, slot_date, slot_time)
);

-- AGENDAMENTOS
create table bookings (
  id uuid default gen_random_uuid() primary key,
  subscriber_id uuid references subscribers(id),
  salon_id uuid references salons(id),
  slot_id uuid references available_slots(id),
  procedure_name text not null,
  booking_date date not null,
  booking_time time not null,
  status text check (status in ('pending','confirmed','completed','cancelled')) default 'pending',
  platform_value numeric(10,2),
  notes text,
  created_at timestamptz default now()
);

-- FINANCEIRO — Pagamentos aos salões
create table salon_payments (
  id uuid default gen_random_uuid() primary key,
  salon_id uuid references salons(id),
  booking_id uuid references bookings(id),
  amount numeric(10,2) not null,
  status text check (status in ('pending','paid')) default 'pending',
  payment_date date,
  created_at timestamptz default now()
);

-- =============================================
-- ROW LEVEL SECURITY (básico para MVP)
-- =============================================
alter table subscribers enable row level security;
alter table salons enable row level security;
alter table bookings enable row level security;
alter table available_slots enable row level security;

-- Assinante vê apenas seus próprios dados
create policy "subscriber own data" on subscribers
  for all using (auth.uid() = id);

-- Assinante vê bookings próprios
create policy "subscriber own bookings" on bookings
  for all using (
    subscriber_id = auth.uid()
  );

-- Salão vê apenas seus slots
create policy "salon own slots" on available_slots
  for all using (
    salon_id in (select id from salons where email = auth.email())
  );

-- Slots disponíveis são públicos para assinantes lerem
create policy "public read available slots" on available_slots
  for select using (is_booked = false);

-- Salões são visíveis para todos (catálogo)
create policy "public read active salons" on salons
  for select using (status = 'active');
