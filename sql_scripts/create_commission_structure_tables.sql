-- Create carriers table
CREATE TABLE IF NOT EXISTS carriers (
    carrier_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    carrier_name TEXT UNIQUE NOT NULL,
    naic_code TEXT,
    producer_code TEXT,
    parent_company TEXT,
    status TEXT DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create MGAs table
CREATE TABLE IF NOT EXISTS mgas (
    mga_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    mga_name TEXT UNIQUE NOT NULL,
    contact_info JSONB DEFAULT '{}',
    appointment_date DATE,
    status TEXT DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create carrier-MGA relationships table
CREATE TABLE IF NOT EXISTS carrier_mga_relationships (
    relationship_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    carrier_id UUID NOT NULL REFERENCES carriers(carrier_id) ON DELETE CASCADE,
    mga_id UUID NOT NULL REFERENCES mgas(mga_id) ON DELETE CASCADE,
    is_direct BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(carrier_id, mga_id)
);

-- Create commission rules table
CREATE TABLE IF NOT EXISTS commission_rules (
    rule_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    carrier_id UUID NOT NULL REFERENCES carriers(carrier_id) ON DELETE CASCADE,
    mga_id UUID REFERENCES mgas(mga_id) ON DELETE CASCADE,
    state TEXT DEFAULT 'FL',
    policy_type TEXT,
    term_months INTEGER,
    new_rate DECIMAL(5,2) NOT NULL CHECK (new_rate >= 0 AND new_rate <= 100),
    renewal_rate DECIMAL(5,2) CHECK (renewal_rate >= 0 AND renewal_rate <= 100),
    payment_terms TEXT CHECK (payment_terms IN ('Advanced', 'As Earned')),
    rule_description TEXT,
    rule_priority INTEGER GENERATED ALWAYS AS (
        CASE 
            WHEN mga_id IS NOT NULL THEN 1000 
            ELSE 0 
        END +
        CASE 
            WHEN state IS NOT NULL THEN 100 
            ELSE 0 
        END +
        CASE 
            WHEN policy_type IS NOT NULL THEN 10 
            ELSE 0 
        END +
        CASE 
            WHEN term_months IS NOT NULL THEN 1 
            ELSE 0 
        END
    ) STORED,
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add new columns to policies table (all nullable for backward compatibility)
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS carrier_id UUID REFERENCES carriers(carrier_id),
ADD COLUMN IF NOT EXISTS mga_id UUID REFERENCES mgas(mga_id),
ADD COLUMN IF NOT EXISTS commission_rule_id UUID REFERENCES commission_rules(rule_id),
ADD COLUMN IF NOT EXISTS commission_rate_override DECIMAL(5,2);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_carriers_name ON carriers(carrier_name);
CREATE INDEX IF NOT EXISTS idx_carriers_status ON carriers(status);
CREATE INDEX IF NOT EXISTS idx_mgas_name ON mgas(mga_name);
CREATE INDEX IF NOT EXISTS idx_mgas_status ON mgas(status);
CREATE INDEX IF NOT EXISTS idx_commission_rules_carrier ON commission_rules(carrier_id);
CREATE INDEX IF NOT EXISTS idx_commission_rules_mga ON commission_rules(mga_id);
CREATE INDEX IF NOT EXISTS idx_commission_rules_priority ON commission_rules(rule_priority DESC);
CREATE INDEX IF NOT EXISTS idx_policies_carrier ON policies(carrier_id);
CREATE INDEX IF NOT EXISTS idx_policies_mga ON policies(mga_id);

-- Create update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update trigger to all new tables
CREATE TRIGGER update_carriers_updated_at BEFORE UPDATE ON carriers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_mgas_updated_at BEFORE UPDATE ON mgas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_commission_rules_updated_at BEFORE UPDATE ON commission_rules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();