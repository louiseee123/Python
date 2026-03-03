$env:DATABASE_URL = "postgresql://neondb_owner:npg_q0Eh9UuFJjWc@ep-falling-sunset-airjnjq5-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
python quickserve/manage.py migrate
