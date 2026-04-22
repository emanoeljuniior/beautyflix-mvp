# ✨ BeautyFlix MVP

> Beleza por assinatura — Joinville/SC  
> Inspirado no modelo GymPass/TotalPass, aplicado ao mercado de beleza.

---

## 🏗️ Estrutura do Projeto

```
beautyflix/
├── app.py                  ← App principal (Streamlit)
├── supabase_client.py      ← Integração com banco de dados
├── supabase_schema.sql     ← Schema completo do banco
├── requirements.txt        ← Dependências
├── BeautyFlix_Colab.ipynb  ← Notebook para rodar no Google Colab
└── README.md
```

---

## 🚀 Como Rodar

### Opção 1 — Google Colab (mais fácil, zero instalação)

1. Abra `BeautyFlix_Colab.ipynb` no Google Colab
2. Na célula 3, cole o conteúdo de `app.py`
3. Execute todas as células em ordem
4. Clique no link `.loca.lt` que aparecer

### Opção 2 — Localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Opção 3 — Streamlit Cloud (deploy gratuito)

1. Faça fork do repositório no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório e faça deploy em 1 clique
4. Configure as variáveis de ambiente no painel do Streamlit Cloud

---

## 🗄️ Configurar Supabase (banco de dados gratuito)

1. Crie conta em [supabase.com](https://supabase.com) — **gratuito**
2. Crie um novo projeto
3. Vá em **SQL Editor** e cole o conteúdo de `supabase_schema.sql`
4. Execute o script
5. Em **Settings → API**, copie a `URL` e a `anon/public key`
6. Configure como variáveis de ambiente:
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJxxxxx...
   ```

> ⚠️ **Sem configurar Supabase**, o app funciona com dados simulados (mock) — perfeito para demonstração e testes iniciais.

---

## 👤 Perfis do MVP

### Assinante (cliente final)
- **Login:** ana@email.com / 123456
- Ver plano atual e procedimentos disponíveis
- Buscar salões por procedimento e data
- Agendar horários disponíveis
- Gerenciar/cancelar agendamentos
- Trocar de plano

### Salão Parceiro
- **Login:** studio@bella.com / 123456
- Dashboard com métricas do mês
- Gerenciar disponibilidade de horários
- Ver e confirmar reservas de assinantes
- Extrato financeiro com valor por procedimento

---

## 💼 Modelo de Negócio BeautyFlix

| Plano     | Preço/mês | Procedimentos |
|-----------|-----------|---------------|
| Starter   | R$ 79,90  | 4/mês         |
| Plus      | R$ 139,90 | 8/mês         |
| Premium   | R$ 199,90 | 14/mês        |

**Para os salões:**
- Cadastro gratuito na plataforma
- Recebem valor líquido por procedimento (abaixo do preço de balcão)
- Benefícios: novos clientes, ocupação de horários ociosos, marketing gratuito
- Obrigação contratual: mínimo de 2 horários/dia para assinantes

---

## 🗺️ Stack Gratuita Recomendada

| Componente       | Ferramenta         | Custo       |
|------------------|--------------------|-------------|
| Frontend/App     | Streamlit          | Gratuito    |
| Banco de dados   | Supabase           | Gratuito    |
| Deploy           | Streamlit Cloud    | Gratuito    |
| Autenticação     | Supabase Auth      | Gratuito    |
| Armazenamento    | Supabase Storage   | Gratuito    |
| Geolocalização   | Nominatim (OpenStreetMap) | Gratuito |
| Notificações     | Supabase Edge Functions + SendGrid free | Gratuito |

---

## 🔮 Próximos Passos (pós-MVP)

- [ ] Autenticação real com Supabase Auth
- [ ] Geolocalização com mapa interativo (Folium/Leaflet)
- [ ] Notificações por e-mail/WhatsApp (confirmação de agendamento)
- [ ] Pagamentos com Stripe ou Pagar.me
- [ ] Avaliações de procedimentos pós-atendimento
- [ ] App mobile com React Native / Flutter
- [ ] Dashboard admin para gestão da plataforma

---

## 📞 Contato

Desenvolvido como MVP para validação do modelo BeautyFlix em Joinville/SC.
