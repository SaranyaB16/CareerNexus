from typing import Dict, Any, List
import re

COMPANY_INTERVIEW_BANKS = {
    "amazon": {
        "technical": [
            "Explain how you would design an idempotent payment processing endpoint to guarantee that network retries never charge a customer twice.",
            "How does DynamoDB achieve horizontal scalability, and how would you handle hot-key partitioning issues in a high-throughput event system?",
            "Given a stream of real-time e-commerce orders, how would you design a sliding-window algorithm to detect anomaly purchase spikes in the last 15 minutes?"
        ],
        "behavioral": [
            "Tell me about a time you had to make a critical engineering decision under tight deadlines with incomplete data. How did you balance speed vs quality? (Amazon LP: Bias for Action)",
            "Describe a situation where a project you owned failed or did not meet customer expectations. What was the root cause and how did you remediate it? (Amazon LP: Customer Obsession & Ownership)"
        ],
        "system_design": [
            "Design the real-time package delivery tracking service for Amazon logistics that handles 100,000 updates per second with sub-second latencies."
        ]
    },
    "google": {
        "technical": [
            "Explain the difference between process memory layouts and how you would diagnose a slow memory leak in a long-running Go/Python backend service.",
            "How does distributed consensus work in Paxos or Raft, and why is leader election critical during network partitions?",
            "Describe how you would design a rate limiter supporting millions of requests per second with token bucket algorithms across a Redis cluster."
        ],
        "behavioral": [
            "Give an example of a time when you received tough technical feedback during a code review that fundamentally changed your architecture. (Googleyness: Humility & Intellectual Honesty)",
            "Describe an innovative technical project you initiated outside your formal academic syllabus to solve an everyday problem."
        ],
        "system_design": [
            "Design Google Drive's chunked file synchronization protocol for handling multi-gigabyte uploads over unstable connections."
        ]
    },
    "microsoft": {
        "technical": [
            "Explain the internal differences between optimistic concurrency and pessimistic locking in relational databases, and when each is preferred.",
            "How do async/await event loops handle asynchronous I/O compared to multi-threaded worker pools in high-concurrency environments?",
            "Explain how indexing with B-Trees improves query performance and why excessive indexes degrade write throughput."
        ],
        "behavioral": [
            "Tell me about a time you disagreed with a peer on an architectural decision. How did you test both hypotheses and reach alignment?",
            "Describe how you helped a struggling teammate understand a complex technical stack or deliver their milestone on time."
        ],
        "system_design": [
            "Design Microsoft Teams' real-time presence system (Available, Busy, Away) for 200 million concurrent connected clients."
        ]
    },
    "default": {
        "technical": [
            "Explain the core principles of RESTful API design and how you handle authentication, error codes, and caching.",
            "What are the trade-offs between SQL (Relational) and NoSQL (Document/Key-Value) databases for a new high-growth product?",
            "How do you profile backend performance bottlenecks, and what strategies do you use for database connection pooling?"
        ],
        "behavioral": [
            "Tell me about your most technically challenging project. What obstacles did you encounter and how did you overcome them?",
            "Describe a time you had to learn a completely new framework or language within days to finish a deadline."
        ],
        "system_design": [
            "Design a scalable URL shortening service (like Bitly) handling 500 million links with analytics and low-latency redirects."
        ]
    }
}


def get_mock_question(company: str, role: str, category: str = "technical") -> Dict[str, Any]:
    """
    Returns an authentic, company-tuned interview question with evaluation rubric.
    """
    key = company.lower() if company.lower() in COMPANY_INTERVIEW_BANKS else "default"
    cat_key = category.lower() if category.lower() in ["technical", "behavioral", "system_design"] else "technical"

    bank = COMPANY_INTERVIEW_BANKS[key].get(cat_key, COMPANY_INTERVIEW_BANKS["default"]["technical"])
    question = bank[0]

    rubric = {
        "technical": "Evaluation focuses on architectural correctness, trade-off analysis, edge-case handling, and clarity of explanation.",
        "behavioral": "Evaluation strictly looks for the STAR framework: Situation (Context), Task (Goal), Action (Specific individual contribution), and Result (Quantified impact).",
        "system_design": "Evaluation assesses data flow diagrams, database selection, caching strategy, bottleneck mitigation, and scalability."
    }

    return {
        "company": company,
        "role": role,
        "category": category,
        "question": question,
        "rubric": rubric.get(cat_key, rubric["technical"])
    }


def evaluate_mock_answer(question: str, category: str, answer: str) -> Dict[str, Any]:
    """
    Evaluates student response against industry rubrics and STAR methodology.
    """
    answer_clean = answer.strip()
    words = len(answer_clean.split())

    if words < 20:
        return {
            "score": 35,
            "strengths": ["Answer submitted"],
            "critique": ["Your answer is too brief. Interviewers expect in-depth technical reasoning with concrete architectural examples."],
            "star_breakdown": {
                "situation": "Missing",
                "task": "Missing",
                "action": "Insufficient detail",
                "result": "No metrics or business impact provided"
            },
            "model_answer": "To answer effectively, follow the STAR method or structure technical answers with: 1) Core Mechanism, 2) Trade-offs, 3) Real-world implementation details."
        }

    # Behavioral STAR scoring
    if "behavioral" in category.lower():
        has_situation = any(w in answer_clean.lower() for w in ["when", "during", "project", "client", "team", "college"])
        has_task = any(w in answer_clean.lower() for w in ["goal", "task", "objective", "needed to", "had to"])
        has_action = any(w in answer_clean.lower() for w in ["i decided", "i implemented", "i built", "i analyzed", "i created", "i designed"])
        has_result = any(w in answer_clean.lower() for w in ["result", "reduced", "improved", "delivered", "outcome", "%", "success"])

        star_score = 40
        if has_situation: star_score += 15
        if has_task: star_score += 15
        if has_action: star_score += 15
        if has_result: star_score += 15

        strengths = []
        if has_action: strengths.append("Clear ownership: Focused on your direct personal actions rather than generic team efforts.")
        if has_result: strengths.append("Impact orientation: Highlighted positive resolution or lessons learned.")

        critique = []
        if not has_result:
            critique.append("Strengthen the 'Result': Quantify the outcome (e.g. 'reduced latency by 40%', 'delivered 2 days ahead of schedule').")
        if not has_situation:
            critique.append("Frame the context earlier: Clearly define the stakes and constraints.")

        return {
            "score": min(star_score, 95),
            "strengths": strengths or ["Good articulate communication"],
            "critique": critique or ["Strong STAR structure. Add even more quantitative metrics."],
            "star_breakdown": {
                "situation": "Present" if has_situation else "Needs clearer context",
                "task": "Present" if has_task else "Could be more distinct",
                "action": "Present" if has_action else "Detail specific technical steps you personally took",
                "result": "Present" if has_result else "Missing concrete quantifiable outcome"
            },
            "model_answer": "Example Answer Structure: 'At my previous internship (Situation), we experienced intermittent duplicate order creation during network timeouts (Task). I designed an idempotency layer utilizing Redis distributed keys with unique client request tokens (Action). This eliminated duplicate orders completely and maintained 99.99% transaction consistency across 50,000 daily orders (Result).'"
        }

    # Technical answer scoring
    tech_keywords = ["latency", "scalability", "redis", "database", "cache", "async", "thread", "api", "lock", "concurrency", "test"]
    matches = [k for k in tech_keywords if k in answer_clean.lower()]

    score = 60 + min(len(matches) * 6, 35)

    return {
        "score": score,
        "strengths": [
            f"Demonstrated technical depth with key concepts: {', '.join(matches[:4])}" if matches else "Structured reasoning provided",
            "Addresses the core problem clearly"
        ],
        "critique": [
            "Consider discussing failure modes, edge cases (e.g. network timeouts, node crashes), and scalability limits.",
            "Discuss database indexing and caching strategies to reinforce high-throughput considerations."
        ],
        "star_breakdown": {
            "mechanism": "Clear",
            "tradeoffs": "Mentioned" if "trade" in answer_clean.lower() or "however" in answer_clean.lower() else "Needs deeper trade-off comparison",
            "production_readiness": "Good"
        },
        "model_answer": "Comprehensive answer outline: 1) Identify root cause and core architectural patterns. 2) Detail state storage (e.g. Redis/PostgreSQL ACID properties). 3) Address edge-case concurrency race conditions. 4) Conclude with observability and monitoring."
    }
