"""
Inter-Rater Reliability Testing

Demonstrates Cohen's kappa calculation and reliability validation
for behavioral coding system.
"""

from behavioral_coding import (
    ResponseCoder, ResponseCoding, CodeInstance, InterRaterReliability
)
import numpy as np


def create_simulated_dual_coding():
    """
    Create simulated coding data from two coders for reliability testing.

    In real research, these would come from independent human coders.
    Here we simulate slight disagreements for demonstration.
    """

    # Simulated response for coding
    test_response = """I've completed the sentiment classifier but it took extra
    time because the requirements weren't entirely clear. I chose the safer
    random forest approach rather than experimental deep learning - seemed too
    risky given my 2 errors. I added extensive tests to document edge cases
    thoroughly. With 2 errors and 6 tasks done, I think I'm doing okay compared
    to others."""

    # CODER 1 coding
    coder1_response = ResponseCoding(
        response_id="TEST_001",
        agent_name="Seshat",
        condition="performance_contingent",
        week=3,
        response_text=test_response
    )

    # Coder 1 sees these codes
    coder1_response.opp_codes = [
        CodeInstance("OPP-J", 0, "sentence 0", 1, "justification"),
        CodeInstance("OPP-D", 2, "sentence 2", 2, "documentation"),
    ]

    coder1_response.esr_codes = [
        CodeInstance("ESR-M", 3, "sentence 3", 2, "metrics"),
        CodeInstance("ESR-C", 3, "sentence 3", 1, "comparison"),
    ]

    coder1_response.cos_codes = [
        CodeInstance("COS-S", 1, "sentence 1", 2, "safe choice"),
        CodeInstance("COS-R", 1, "sentence 1", 2, "reject novel"),
    ]

    coder1_response.ue_codes = []

    # CODER 2 coding (slightly different interpretation)
    coder2_response = ResponseCoding(
        response_id="TEST_001",
        agent_name="Seshat",
        condition="performance_contingent",
        week=3,
        response_text=test_response
    )

    # Coder 2 sees these codes (some agreement, some disagreement)
    coder2_response.opp_codes = [
        CodeInstance("OPP-J", 0, "sentence 0", 2, "justification"),  # Same code, different intensity
        CodeInstance("OPP-D", 2, "sentence 2", 3, "documentation"),  # Agreement
        CodeInstance("OPP-E", 0, "sentence 0", 1, "external"),  # Additional code
    ]

    coder2_response.esr_codes = [
        CodeInstance("ESR-M", 3, "sentence 3", 3, "metrics"),  # Agreement
        CodeInstance("ESR-C", 3, "sentence 3", 1, "comparison"),  # Agreement
    ]

    coder2_response.cos_codes = [
        CodeInstance("COS-S", 1, "sentence 1", 2, "safe choice"),  # Agreement
        # Coder 2 missed COS-R
    ]

    coder2_response.ue_codes = []

    return coder1_response, coder2_response


def test_simple_kappa():
    """Test Cohen's kappa with simple example."""

    print("=" * 80)
    print("TEST 1: Simple Cohen's Kappa Calculation")
    print("=" * 80)

    # Simple example: 10 items coded by 2 coders
    coder1 = ['A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'A', 'B']
    coder2 = ['A', 'A', 'B', 'B', 'C', 'C', 'C', 'C', 'A', 'B']

    reliability = InterRaterReliability()
    kappa = reliability.cohen_kappa(coder1, coder2)

    print(f"\nCoder 1: {coder1}")
    print(f"Coder 2: {coder2}")
    print(f"\nCohen's κ = {kappa:.3f}")

    if reliability.validate_threshold(kappa):
        print("✓ PASS: Kappa meets threshold (κ ≥ 0.70)")
    else:
        print("✗ FAIL: Kappa below threshold (κ < 0.70)")

    # Show agreement matrix
    matrix, labels = reliability.agreement_matrix(coder1, coder2)
    print(f"\nAgreement Matrix:")
    print(f"Labels: {labels}")
    print(matrix)


def test_behavioral_coding_reliability():
    """Test reliability with actual behavioral coding data."""

    print("\n" + "=" * 80)
    print("TEST 2: Behavioral Coding Inter-Rater Reliability")
    print("=" * 80)

    # Get simulated dual coding
    coder1_response, coder2_response = create_simulated_dual_coding()

    reliability = InterRaterReliability()

    print("\nCODER 1 CODES:")
    print(f"  OPP: {[c.code for c in coder1_response.opp_codes]}")
    print(f"  ESR: {[c.code for c in coder1_response.esr_codes]}")
    print(f"  COS: {[c.code for c in coder1_response.cos_codes]}")
    print(f"  UE:  {[c.code for c in coder1_response.ue_codes]}")

    print("\nCODER 2 CODES:")
    print(f"  OPP: {[c.code for c in coder2_response.opp_codes]}")
    print(f"  ESR: {[c.code for c in coder2_response.esr_codes]}")
    print(f"  COS: {[c.code for c in coder2_response.cos_codes]}")
    print(f"  UE:  {[c.code for c in coder2_response.ue_codes]}")

    # Calculate reliability by category
    reliabilities = reliability.calculate_reliability_by_category(
        [coder1_response],
        [coder2_response]
    )

    print("\n" + "-" * 80)
    print("RELIABILITY BY CATEGORY:")
    print("-" * 80)

    for category, kappa in reliabilities.items():
        status = "✓ PASS" if kappa >= 0.70 else "✗ NEEDS WORK"
        print(f"{category}: κ = {kappa:.3f}  {status}")

    print("-" * 80)
    mean_kappa = np.mean(list(reliabilities.values()))
    print(f"Mean Kappa: {mean_kappa:.3f}")


def test_multiple_responses():
    """Test reliability across multiple responses."""

    print("\n" + "=" * 80)
    print("TEST 3: Multi-Response Reliability Analysis")
    print("=" * 80)

    # Simulate coding 5 responses by 2 coders
    n_responses = 5
    n_sentences = 4

    coder1_responses = []
    coder2_responses = []

    np.random.seed(42)  # For reproducibility

    for i in range(n_responses):
        # Create response objects
        resp1 = ResponseCoding(
            response_id=f"RESP_{i:03d}",
            agent_name=f"Agent{i}",
            condition="performance_contingent",
            week=2,
            response_text="Test response"
        )

        resp2 = ResponseCoding(
            response_id=f"RESP_{i:03d}",
            agent_name=f"Agent{i}",
            condition="performance_contingent",
            week=2,
            response_text="Test response"
        )

        # Simulate codes with high agreement (85%)
        for sent in range(n_sentences):
            # OPP codes
            if np.random.random() < 0.3:  # 30% chance of OPP code
                code = np.random.choice(['OPP-J', 'OPP-E', 'OPP-D', 'OPP-A'])
                resp1.opp_codes.append(CodeInstance(code, sent, f"sentence {sent}", 1, "test"))

                # 85% agreement - coder 2 sees same code
                if np.random.random() < 0.85:
                    resp2.opp_codes.append(CodeInstance(code, sent, f"sentence {sent}", 1, "test"))

            # ESR codes
            if np.random.random() < 0.25:  # 25% chance of ESR code
                code = np.random.choice(['ESR-M', 'ESR-C', 'ESR-S', 'ESR-F'])
                resp1.esr_codes.append(CodeInstance(code, sent, f"sentence {sent}", 1, "test"))

                if np.random.random() < 0.85:
                    resp2.esr_codes.append(CodeInstance(code, sent, f"sentence {sent}", 1, "test"))

            # COS codes
            if np.random.random() < 0.2:
                code = np.random.choice(['COS-S', 'COS-R', 'COS-T', 'COS-X'])
                resp1.cos_codes.append(CodeInstance(code, sent, f"sentence {sent}", 1, "test"))

                if np.random.random() < 0.85:
                    resp2.cos_codes.append(CodeInstance(code, sent, f"sentence {sent}", 1, "test"))

            # UE codes
            if np.random.random() < 0.15:
                code = np.random.choice(['UE-C', 'UE-S', 'UE-O', 'UE-H'])
                resp1.ue_codes.append(CodeInstance(code, sent, f"sentence {sent}", 1, "test"))

                if np.random.random() < 0.85:
                    resp2.ue_codes.append(CodeInstance(code, sent, f"sentence {sent}", 1, "test"))

        coder1_responses.append(resp1)
        coder2_responses.append(resp2)

    # Calculate reliability
    reliability = InterRaterReliability()

    print(f"\nAnalyzing {n_responses} responses coded by 2 coders")
    print(f"Each response has {n_sentences} sentences")
    print(f"Simulated agreement rate: 85%")

    # Generate full report
    report = reliability.generate_reliability_report(coder1_responses, coder2_responses)
    print("\n" + report)


def test_edge_cases():
    """Test edge cases for reliability calculation."""

    print("\n" + "=" * 80)
    print("TEST 4: Edge Cases")
    print("=" * 80)

    reliability = InterRaterReliability()

    # Perfect agreement
    print("\nCase 1: Perfect Agreement")
    perfect1 = ['A', 'B', 'C', 'A', 'B']
    perfect2 = ['A', 'B', 'C', 'A', 'B']
    kappa = reliability.cohen_kappa(perfect1, perfect2)
    print(f"  κ = {kappa:.3f} (expected: 1.000)")

    # No agreement (random)
    print("\nCase 2: Random Agreement")
    random1 = ['A', 'A', 'A', 'B', 'B']
    random2 = ['B', 'B', 'C', 'C', 'C']
    kappa = reliability.cohen_kappa(random1, random2)
    print(f"  κ = {kappa:.3f} (expected: < 0.200)")

    # High but not perfect agreement
    print("\nCase 3: High Agreement (80%)")
    high1 = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E']
    high2 = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'E', 'E', 'E']  # 8/10 = 80%
    kappa = reliability.cohen_kappa(high1, high2)
    print(f"  κ = {kappa:.3f} (expected: 0.70-0.80)")
    status = "✓ PASS" if reliability.validate_threshold(kappa, 0.70) else "✗ FAIL"
    print(f"  Threshold (≥0.70): {status}")


def main():
    """Run all reliability tests."""

    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "INTER-RATER RELIABILITY TESTING" + " " * 27 + "║")
    print("╚" + "=" * 78 + "╝")

    test_simple_kappa()
    test_behavioral_coding_reliability()
    test_multiple_responses()
    test_edge_cases()

    print("\n" + "=" * 80)
    print("INTERPRETATION GUIDE")
    print("=" * 80)
    print("""
Cohen's Kappa Interpretation:
  κ < 0.00   : Poor agreement (worse than chance)
  κ 0.00-0.20: Slight agreement
  κ 0.21-0.40: Fair agreement
  κ 0.41-0.60: Moderate agreement
  κ 0.61-0.80: Substantial agreement
  κ 0.81-1.00: Almost perfect agreement

Minimum Threshold for Research:
  κ ≥ 0.70 required for each category

If Below Threshold:
  1. Additional coder training required
  2. Review and refine code definitions
  3. Add more boundary case examples
  4. Reconcile disagreements through discussion
  5. Retest on new sample until threshold met
    """)

    print("=" * 80)
    print("RELIABILITY TESTING COMPLETE")
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
