from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey, Float, Boolean, Text, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class ShipStatus(str, enum.Enum):
    open = "open"
    full = "full"
    delivered = "delivered"

class PricingType(str, enum.Enum):
    FOB = "FOB"
    CIF = "CIF"

class AlertStatus(str, enum.Enum):
    active = "active"
    triggered = "triggered"
    disabled = "disabled"

class Currency(str, enum.Enum):
    USD = "USD"
    TND = "TND"

class ChannelType(str, enum.Enum):
    contract = "contract"
    ship = "ship"
    grade = "grade"
    private = "private"

class FixingApprovalStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True)
    can_fix_direct = Column(Boolean, default=False)
    requires_validation = Column(Boolean, default=True)
    can_view_all = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role")

class Contract(Base):
    __tablename__ = "contracts"
    contract_id = Column(Integer, primary_key=True)
    supplier = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    freight_usd_mt = Column(Float)
    grades_allowed = Column(Text)  # store as CSV for SQLite portability
    min_qty_per_ship = Column(Integer)
    max_grades_per_ship = Column(Integer)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class Ship(Base):
    __tablename__ = "ships"
    ship_id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"))
    ship_name = Column(String)
    shipment_month = Column(String)  # YYYY-MM
    status = Column(Enum(ShipStatus), default=ShipStatus.open)
    created_at = Column(DateTime, default=datetime.utcnow)

class Grade(Base):
    __tablename__ = "grades"
    grade_id = Column(Integer, primary_key=True)
    grade_name = Column(String)
    code_reuters = Column(String)
    pricing_type = Column(Enum(PricingType))
    origin = Column(String)

class Fixing(Base):
    __tablename__ = "fixings"
    fixing_id = Column(Integer, primary_key=True)
    ship_id = Column(Integer, ForeignKey("ships.ship_id"))
    grade_id = Column(Integer, ForeignKey("grades.grade_id"))
    supplier = Column(String)
    fixing_date = Column(Date)
    quantity_mt = Column(Integer)
    freight_usd_mt = Column(Float)
    cfr_price_usd_mt = Column(Float)
    created_by = Column(Integer, ForeignKey("users.user_id"))

class FixingApproval(Base):
    __tablename__ = "fixing_approvals"
    approval_id = Column(Integer, primary_key=True)
    fixing_id = Column(Integer, ForeignKey("fixings.fixing_id"))
    requested_by = Column(Integer, ForeignKey("users.user_id"))
    approved_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    status = Column(Enum(FixingApprovalStatus), default=FixingApprovalStatus.pending)
    decision_date = Column(DateTime, nullable=True)

class CDSBOSpot(Base):
    __tablename__ = "cdsbo_spot"
    spot_id = Column(Integer, primary_key=True)
    supplier = Column(String)
    purchase_type = Column(Enum("import", "local", name="purchase_type"))
    vessel_name = Column(String, nullable=True)
    purchase_date = Column(Date)
    quantity_mt = Column(Integer)
    freight = Column(Float)
    cfr_price_usd_mt = Column(Float)
    created_by = Column(Integer, ForeignKey("users.user_id"))

class MarketData(Base):
    __tablename__ = "market_data"
    market_id = Column(Integer, primary_key=True)
    grade_id = Column(Integer, ForeignKey("grades.grade_id"))
    date = Column(Date)
    price_fob_cif = Column(Float)
    usd_tnd_rate = Column(Float)
    source = Column(String)

class Alert(Base):
    __tablename__ = "alerts"
    alert_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    grade_id = Column(Integer, ForeignKey("grades.grade_id"))
    target_price_usd_mt = Column(Float)
    currency = Column(Enum(Currency), default=Currency.USD)
    status = Column(Enum(AlertStatus), default=AlertStatus.active)

class Setting(Base):
    __tablename__ = "settings"
    setting_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    email_recipients = Column(Text)  # CSV
    excel_export_path = Column(String)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    message_id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.user_id"))
    channel_type = Column(Enum(ChannelType))
    channel_id = Column(Integer)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    linked_fixing_id = Column(Integer, ForeignKey("fixings.fixing_id"), nullable=True)
