-- Tourism Website Database Tables for Supabase

-- 1. Guide Bookings Table
CREATE TABLE guide_bookings (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    preferred_language TEXT,
    places_of_interest TEXT[],
    date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Transport Bookings Table
CREATE TABLE transport_bookings (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    pickup_location TEXT,
    destination TEXT,
    vehicle_type TEXT,
    datetime TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Activity Bookings Table
CREATE TABLE activity_bookings (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    activity TEXT,
    location TEXT,
    participants INTEGER,
    date DATE,
    special_requirements TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);