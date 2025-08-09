-- Minimal seed for PostgreSQL
INSERT INTO grades (grade_id, grade_name, code_reuters, pricing_type, origin) VALUES
(1,'CDSBO','CDSBO=R','CIF','AR'),
(2,'RBD Palm Olein','POL=R','FOB','MY')
ON CONFLICT DO NOTHING;

INSERT INTO market_data (market_id, grade_id, date, price_fob_cif, usd_tnd_rate, source) VALUES
(1,1,'2025-07-15',1050.0,3.2,'TEST'),
(2,2,'2025-07-15',960.0,3.2,'TEST')
ON CONFLICT DO NOTHING;
