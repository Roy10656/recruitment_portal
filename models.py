from sqlalchemy import Column, Integer, String

from database import Base


class Student(Base):
    __tablename__ = "students"

    # Candidate Details
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    mobile = Column(String(15), unique=True, nullable=False)
    department = Column(String(50), nullable=False)
    percentage = Column(Integer, nullable=False)
    active_backlogs = Column(String(10), nullable=False)
    prefered_techstack = Column(String(100), nullable=True)

    # Eligibility Engine
    eligibility = Column(String(30), nullable=True)

    # Round 1 Evaluation
    requirement_understanding = Column(Integer, nullable=True)
    feature_implementation = Column(Integer, nullable=True)
    validation_edge_cases = Column(Integer, nullable=True)
    code_structure = Column(Integer, nullable=True)
    ai_usage = Column(Integer, nullable=True)

    # Total Round 1 Score (Out of 100)
    round_1_score = Column(Integer, nullable=True)

    # Final HR Decision
    final_shortlist = Column(String(30), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "mobile": self.mobile,
            "department": self.department,
            "percentage": self.percentage,
            "active_backlogs": self.active_backlogs,
            "prefered_techstack": self.prefered_techstack,
            "eligibility": self.eligibility,
            "requirement_understanding": self.requirement_understanding,
            "feature_implementation": self.feature_implementation,
            "validation_edge_cases": self.validation_edge_cases,
            "code_structure": self.code_structure,
            "ai_usage": self.ai_usage,
            "round_1_score": self.round_1_score,
            "final_shortlist": self.final_shortlist
        }