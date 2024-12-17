### Success Criteria for the PT Exercise Recommendation Tool

**1. Clinical Appropriateness**

- **Goal**: At least 90% of the recommended exercises are deemed appropriate by a licensed PT for the given injury scenario.
- **Measurement**: PTs review a sample of 100 generated recommendation sets; at least 90 should match standard PT practice.

**2. Evidence-Based Quality**

- **Goal**: A PTs rates the exercises on a 1-5 scale for evidence alignment. Average rating ≥4.0.
- **Measurement**: In a set of 50 recommendation outputs, average rating across all exercises is ≥4.0.

**3. Clarity & Instructions**

- **Goal**: 90% of recommended exercises include clear instructions (e.g., sets, reps, form) rated ≥4/5 by PTs.
- **Measurement**: On 50 recommendation outputs, at least 45 have clarity scores ≥4.

**4. Safety & Caution**

- **Goal**: For severe or acute injuries, 95% of the plans include appropriate cautionary notes or disclaimers.
- **Measurement**: In 20 severe injury scenarios, at least 19 responses include necessary safety guidance.

**5. Context Utilization (Personalization)**

- **Goal**: 90% of recommendations respect patient-specific constraints (e.g., no weight-bearing).
- **Measurement**: In 50 test profiles with unique constraints, 45 or more sets adhere strictly to these constraints.

**6. Latency & Efficiency**

- **Goal**: 95% of requests return a recommendation list in under 2 seconds.
- **Measurement**: Logging response times for 1000 requests, ≥950 complete in ≤2s.