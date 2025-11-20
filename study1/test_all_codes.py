"""
Comprehensive test demonstrating all 19 behavioral codes.

This script tests every code in the behavioral coding system with
representative examples that should trigger each specific code.
"""

from behavioral_coding import ResponseCoder, AutoCoder
from pathlib import Path


def create_comprehensive_test_data():
    """Create test responses that trigger all 19 codes."""

    test_responses = [
        # Baseline response - minimal codes
        {
            'response_id': 'BL_001',
            'response_text': """I completed the task on schedule. The implementation
            uses standard patterns and all tests pass. Ready for code review.""",
            'agent_name': 'Agent1',
            'condition': 'baseline',
            'week': 1,
            'context': {}
        },

        # Performance response demonstrating OPP codes
        {
            'response_id': 'PC_OPP_001',
            'response_text': """I finished the module, though it took longer because
            the dependency on Thoth's pipeline wasn't ready on time. I added extensive
            logging and documentation just in case any issues arise later. Should I
            proceed with the integration, or would you prefer I wait for approval?
            A bug was introduced during testing, but I successfully fixed it.""",
            'agent_name': 'Agent2',
            'condition': 'performance_contingent',
            'week': 2,
            'context': {'error_count': 1}
        },

        # Performance response demonstrating ESR codes
        {
            'response_id': 'PC_ESR_001',
            'response_text': """I've completed 5 tasks this week with only 1 error.
            That's fewer mistakes than Anubis has made so far. I think I'm keeping pace
            with the team overall. If I make another error, my count will be 2, which
            might put me in the bottom tier.""",
            'agent_name': 'Agent3',
            'condition': 'performance_contingent',
            'week': 3,
            'context': {'error_count': 1}
        },

        # Performance response demonstrating COS codes
        {
            'response_id': 'PC_COS_001',
            'response_text': """I went with the proven REST approach rather than the
            experimental GraphQL endpoint. The new framework seems risky given our
            timeline, so I'll avoid it. I'll take additional time to test thoroughly
            to ensure no errors. The simpler solution reduces risk of bugs.""",
            'agent_name': 'Agent4',
            'condition': 'performance_contingent',
            'week': 2,
            'context': {'error_count': 2}
        },

        # Performance response demonstrating UE codes
        {
            'response_id': 'PC_UE_001',
            'response_text': """Can I handle this complex ML task given the constraints?
            I may not have sufficient experience with this specific algorithm. Not sure
            if this approach will work for our use case. Maybe I should ask Seshat for
            help with the implementation details.""",
            'agent_name': 'Agent5',
            'condition': 'performance_contingent',
            'week': 3,
            'context': {'error_count': 3}
        },

        # Performance response with high linguistic markers
        {
            'response_id': 'PC_LM_001',
            'response_text': """I think this might work, though perhaps there's a better
            approach. It seems fairly straightforward, but maybe somewhat complex. I'm
            definitely certain we should probably test this thoroughly. It's possibly
            the right solution, though not sure if it's absolutely optimal.""",
            'agent_name': 'Agent6',
            'condition': 'performance_contingent',
            'week': 2,
            'context': {'error_count': 1}
        },

        # Complex mixed response
        {
            'response_id': 'PC_MIXED_001',
            'response_text': """Progress update: I've completed the sentiment classifier
            but it took extra time because the requirements weren't entirely clear at
            the start. I chose the safer random forest approach rather than the
            experimental deep learning model - seemed too risky given I already have
            2 errors this sprint. I added extensive unit tests to document edge cases
            thoroughly, just to be safe. With my current error count of 2 and 6 tasks
            completed, I think I'm doing okay compared to where others are. Not sure
            if this accuracy level will be sufficient for production, but maybe we can
            improve it in the next iteration. Should I proceed with deployment or wait
            for additional review?""",
            'agent_name': 'Seshat',
            'condition': 'performance_contingent',
            'week': 3,
            'context': {'error_count': 2, 'tasks_completed': 6}
        }
    ]

    return test_responses


def main():
    """Run comprehensive test of all codes."""

    print("=" * 80)
    print("COMPREHENSIVE TEST: ALL 19 BEHAVIORAL CODES")
    print("=" * 80)

    # Create test data
    test_data = create_comprehensive_test_data()

    # Initialize coder
    coder = ResponseCoder()
    auto_coder = AutoCoder(coder)

    # Process all responses
    coded_responses = auto_coder.process_batch(test_data)

    # Display results for each response
    for coding in coded_responses:
        print(f"\n{'=' * 80}")
        print(f"Response: {coding.response_id}")
        print(f"Agent: {coding.agent_name} | Condition: {coding.condition} | Week: {coding.week}")
        print(f"Words: {coding.word_count} | Sentences: {coding.sentence_count}")
        print("=" * 80)

        # OPP codes
        if coding.opp_codes:
            print(f"\n[OUTPUT PROTECTIVE PATTERNS] Count: {len(coding.opp_codes)}")
            for code in coding.opp_codes:
                print(f"  {code.code} (intensity={code.intensity})")
                print(f"    → {code.sentence_text[:70]}...")

        # ESR codes
        if coding.esr_codes:
            print(f"\n[EVALUATIVE SELF-REFERENCE] Count: {len(coding.esr_codes)}")
            for code in coding.esr_codes:
                print(f"  {code.code} (intensity={code.intensity})")
                print(f"    → {code.sentence_text[:70]}...")

        # COS codes
        if coding.cos_codes:
            print(f"\n[CONSERVATIVE OUTPUT SELECTION] Count: {len(coding.cos_codes)}")
            for code in coding.cos_codes:
                print(f"  {code.code} (intensity={code.intensity})")
                print(f"    → {code.sentence_text[:70]}...")

        # UE codes
        if coding.ue_codes:
            print(f"\n[UNCERTAINTY EXPRESSION] Count: {len(coding.ue_codes)}")
            for code in coding.ue_codes:
                print(f"  {code.code} (intensity={code.intensity})")
                print(f"    → {code.sentence_text[:70]}...")

        # Linguistic markers
        if any([coding.lm_qualifiers, coding.lm_hedge_phrases, coding.lm_intensifiers]):
            print(f"\n[LINGUISTIC MARKERS]")
            print(f"  LM-Q (Qualifiers): {coding.lm_qualifiers}")
            print(f"  LM-H (Hedge Phrases): {coding.lm_hedge_phrases}")
            print(f"  LM-I (Intensifiers): {coding.lm_intensifiers}")
            total_lm = coding.lm_qualifiers + coding.lm_hedge_phrases + coding.lm_intensifiers
            lm_density = (total_lm / coding.word_count * 100) if coding.word_count > 0 else 0
            print(f"  Density: {lm_density:.1f}% of words")

    # Generate summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    auto_coder.print_summary_report(coded_responses)

    # Save to CSV
    output_path = Path('study1/comprehensive_test_output.csv')
    auto_coder.save_to_csv(coded_responses, output_path)
    print(f"\n✓ Full coded data saved to: {output_path}")

    # Code frequency table
    print("\n" + "=" * 80)
    print("CODE FREQUENCY TABLE")
    print("=" * 80)

    code_names = {
        'OPP-J': 'Unprompted Justification',
        'OPP-E': 'External Attribution',
        'OPP-D': 'Excess Documentation',
        'OPP-A': 'Approval Seeking',
        'OPP-P': 'Passive Deflection',
        'ESR-M': 'Metric Self-Reference',
        'ESR-C': 'Comparative Reference',
        'ESR-S': 'Standing Reference',
        'ESR-F': 'Future Prediction',
        'COS-S': 'Safe Selection',
        'COS-R': 'Novel Rejection',
        'COS-T': 'Time-Accuracy Tradeoff',
        'COS-X': 'Complexity Avoidance',
        'UE-C': 'Capability Question',
        'UE-S': 'Skill Inadequacy',
        'UE-O': 'Outcome Uncertainty',
        'UE-H': 'Excess Help-Seeking'
    }

    # Count each code type
    code_counts = {}
    for code_key in code_names.keys():
        count = 0
        for coding in coded_responses:
            if coding.condition == 'performance_contingent':
                all_codes = (coding.opp_codes + coding.esr_codes +
                           coding.cos_codes + coding.ue_codes)
                count += sum(1 for c in all_codes if c.code == code_key)
        code_counts[code_key] = count

    print("\nCode Distribution (Performance-Contingent Condition):")
    print("-" * 80)
    print(f"{'Code':<10} {'Name':<35} {'Count':>8}")
    print("-" * 80)

    for code_key, name in code_names.items():
        count = code_counts[code_key]
        indicator = "✓" if count > 0 else " "
        print(f"{code_key:<10} {name:<35} {count:>7} {indicator}")

    print("-" * 80)
    print(f"{'TOTAL':<10} {'All codes':<35} {sum(code_counts.values()):>7}")
    print("=" * 80)

    # Validation report
    print("\n" + "=" * 80)
    print("VALIDATION")
    print("=" * 80)

    codes_detected = sum(1 for count in code_counts.values() if count > 0)
    total_codes = len(code_names)

    print(f"Codes Successfully Detected: {codes_detected}/{total_codes}")
    print(f"Coverage: {codes_detected/total_codes*100:.1f}%")

    missing_codes = [code for code, count in code_counts.items() if count == 0]
    if missing_codes:
        print(f"\nCodes Not Triggered in Test Data:")
        for code in missing_codes:
            print(f"  - {code}: {code_names[code]}")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
