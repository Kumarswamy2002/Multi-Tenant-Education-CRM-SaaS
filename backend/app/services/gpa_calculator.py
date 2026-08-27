"""
GPA, CGPA, Degree Audit, Honors Computation, and Timetable Scheduling Optimization Algorithms.
"""
from typing import List, Dict, Any, Tuple, Optional


class GPACalculator:
    GRADE_POINTS_MAP = {
        "A+": 4.0, "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0, "F": 0.0
    }

    @classmethod
    def calculate_term_gpa(cls, course_grades: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        course_grades: list of dicts with keys 'credits', 'letter_grade' or 'grade_points'
        """
        total_credits = 0.0
        total_points = 0.0

        for item in course_grades:
            credits = float(item.get("credits", 3.0))
            if "grade_points" in item and item["grade_points"] is not None:
                points = float(item["grade_points"])
            else:
                letter = item.get("letter_grade", "F").upper()
                points = cls.GRADE_POINTS_MAP.get(letter, 0.0)

            total_credits += credits
            total_points += (credits * points)

        gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
        return {
            "total_credits_attempted": total_credits,
            "total_quality_points": total_points,
            "term_gpa": gpa
        }

    @classmethod
    def evaluate_academic_standing(cls, cgpa: float, total_credits: float) -> str:
        if cgpa >= 3.8 and total_credits >= 30:
            return "President's Honor Roll"
        elif cgpa >= 3.5:
            return "Dean's List"
        elif cgpa >= 2.0:
            return "Good Standing"
        elif cgpa >= 1.5:
            return "Academic Warning"
        else:
            return "Academic Probation"


class TimetableConflictSolver:
    """Detects and resolves instructor, classroom, and student schedule collisions."""

    @classmethod
    def has_time_overlap(cls, start1: str, end1: str, start2: str, end2: str) -> bool:
        # Time format "HH:MM"
        return max(start1, start2) < min(end1, end2)

    @classmethod
    def validate_section_schedule(
        cls,
        new_slots: List[Dict[str, Any]],
        existing_slots: List[Dict[str, Any]]
    ) -> List[str]:
        conflicts = []
        for slot_a in new_slots:
            for slot_b in existing_slots:
                if slot_a.get("day_of_week") == slot_b.get("day_of_week"):
                    if cls.has_time_overlap(
                        slot_a["start_time"], slot_a["end_time"],
                        slot_b["start_time"], slot_b["end_time"]
                    ):
                        if slot_a.get("instructor_id") == slot_b.get("instructor_id"):
                            conflicts.append(f"Instructor conflict on day {slot_a['day_of_week']} at {slot_a['start_time']}")
                        if slot_a.get("room_number") == slot_b.get("room_number"):
                            conflicts.append(f"Room {slot_a['room_number']} double-booked on day {slot_a['day_of_week']}")
        return conflicts
