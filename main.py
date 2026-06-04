def simulate_loan_application(applicant_data: dict, enable_observability: bool = False) -> dict:
    """
    Simulates a simple AI-like loan application approval system.
    Demonstrates the difference between traditional monitoring and observability.
    """
    # --- Internal Model Logic (simplified for demonstration) ---
    # This represents the "black box" of an AI model
    credit_score = applicant_data.get("credit_score", 0)
    income = applicant_data.get("income", 0)
    debt_to_income_ratio = applicant_data.get("debt_to_income_ratio", 0.0)
    employment_years = applicant_data.get("employment_years", 0)

    # Define thresholds (model parameters/rules)
    MIN_CREDIT_SCORE = 650
    MIN_INCOME = 40000
    MAX_DEBT_TO_INCOME_RATIO = 0.4
    MIN_EMPLOYMENT_YEARS = 2

    # Calculate individual criteria fulfillment
    is_credit_score_ok = credit_score >= MIN_CREDIT_SCORE
    is_income_ok = income >= MIN_INCOME
    is_debt_ratio_ok = debt_to_income_ratio <= MAX_DEBT_TO_INCOME_RATIO
    is_employment_ok = employment_years >= MIN_EMPLOYMENT_YEARS

    # Aggregate decision
    approved = (
        is_credit_score_ok and
        is_income_ok and
        is_debt_ratio_ok and
        is_employment_ok
    )

    # --- Traditional Monitoring Output ---
    # This is what traditional monitoring would typically provide:
    # A simple status or final decision. It tells 'what' happened.
    result = {"approved": approved}

    # --- Observability Data Collection ---
    # This section collects internal state and reasoning, providing the 'why'.
    if enable_observability:
        reasons = []
        if not is_credit_score_ok:
            reasons.append(f"Credit score ({credit_score}) below minimum ({MIN_CREDIT_SCORE}).")
        if not is_income_ok:
            reasons.append(f"Income ({income}) below minimum ({MIN_INCOME}).")
        if not is_debt_ratio_ok:
            reasons.append(f"Debt-to-income ratio ({debt_to_income_ratio:.2f}) above maximum ({MAX_DEBT_TO_INCOME_RATIO:.2f}).")
        if not is_employment_ok:
            reasons.append(f"Employment years ({employment_years}) below minimum ({MIN_EMPLOYMENT_YEARS}).")

        if approved:
            reasons.append("All primary criteria met for approval.")
        else:
            reasons.append("Loan rejected due to one or more unmet criteria.")

        # This `observability_data` dictionary is the core of understanding "why".
        # It exposes internal states and decision logic.
        result["observability_data"] = {
            "individual_criteria_met": {
                "credit_score_ok": is_credit_score_ok,
                "income_ok": is_income_ok,
                "debt_ratio_ok": is_debt_ratio_ok,
                "employment_ok": is_employment_ok,
            },
            "thresholds_used": { # Exposing model parameters/rules
                "min_credit_score": MIN_CREDIT_SCORE,
                "min_income": MIN_INCOME,
                "max_debt_to_income_ratio": MAX_DEBT_TO_INCOME_RATIO,
                "min_employment_years": MIN_EMPLOYMENT_YEARS,
            },
            "decision_reasons": reasons, # Explanations for the decision
            "applicant_data_processed": applicant_data # Showing the exact input that led to this decision
        }
    return result

if __name__ == "__main__":
    print("--- Demonstrating Traditional Monitoring vs. Observability in AI ---")
    print("Scenario: A simplified AI-like system for loan application approval.")
    print("Observability helps understand *why* a decision was made, not just *what* the decision was.")

    # --- Applicant 1: Should be approved ---
    applicant_1 = {
        "credit_score": 720,
        "income": 60000,
        "debt_to_income_ratio": 0.25,
        "employment_years": 7
    }
    print("\n--- Applicant 1 (Good Profile - Expected: Approved) ---")
    print("Applicant Data:", applicant_1)

    # Traditional Monitoring View: Only the final outcome
    monitor_result_1 = simulate_loan_application(applicant_1, enable_observability=False)
    print("\n[Traditional Monitoring Result]:")
    print(f"Loan Approved: {monitor_result_1['approved']}")
    # If 'approved' was False, traditional monitoring wouldn't tell us *why*.

    # Observability View: Detailed insights into the decision-making process
    observ_result_1 = simulate_loan_application(applicant_1, enable_observability=True)
    print("\n[Observability Result]:")
    print(f"Loan Approved: {observ_result_1['approved']}")
    print("Observability Data (Why the decision was made):")
    for reason in observ_result_1['observability_data']['decision_reasons']:
        print(f"  - {reason}")
    print("  Individual Criteria Met:", observ_result_1['observability_data']['individual_criteria_met'])

    # --- Applicant 2: Should be rejected (low credit score) ---
    applicant_2 = {
        "credit_score": 600, # Below minimum
        "income": 70000,
        "debt_to_income_ratio": 0.3,
        "employment_years": 8
    }
    print("\n--- Applicant 2 (Low Credit Score - Expected: Rejected) ---")
    print("Applicant Data:", applicant_2)

    # Traditional Monitoring View
    monitor_result_2 = simulate_loan_application(applicant_2, enable_observability=False)
    print("\n[Traditional Monitoring Result]:")
    print(f"Loan Approved: {monitor_result_2['approved']}")
    # Here, 'approved' is False. Without observability, we don't know *why*.

    # Observability View
    observ_result_2 = simulate_loan_application(applicant_2, enable_observability=True)
    print("\n[Observability Result]:")
    print(f"Loan Approved: {observ_result_2['approved']}")
    print("Observability Data (Why the decision was made):")
    for reason in observ_result_2['observability_data']['decision_reasons']:
        print(f"  - {reason}")
    print("  Individual Criteria Met:", observ_result_2['observability_data']['individual_criteria_met'])

    # --- Applicant 3: Should be rejected (high debt-to-income ratio) ---
    applicant_3 = {
        "credit_score": 750,
        "income": 80000,
        "debt_to_income_ratio": 0.5, # Above maximum
        "employment_years": 10
    }
    print("\n--- Applicant 3 (High Debt-to-Income Ratio - Expected: Rejected) ---")
    print("Applicant Data:", applicant_3)

    # Traditional Monitoring View
    monitor_result_3 = simulate_loan_application(applicant_3, enable_observability=False)
    print("\n[Traditional Monitoring Result]:")
    print(f"Loan Approved: {monitor_result_3['approved']}")

    # Observability View
    observ_result_3 = simulate_loan_application(applicant_3, enable_observability=True)
    print("\n[Observability Result]:")
    print(f"Loan Approved: {observ_result_3['approved']}")
    print("Observability Data (Why the decision was made):")
    for reason in observ_result_3['observability_data']['decision_reasons']:
        print(f"  - {reason}")
    print("  Individual Criteria Met:", observ_result_3['observability_data']['individual_criteria_met'])
