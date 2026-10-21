let currentRole = "student";
let activeSessionId = null;

// Initialize when page loads
document.addEventListener("DOMContentLoaded", async () => {
  if (window.lucide) lucide.createIcons();
  await loadInitialData();
  await loadAlerts(1);
  await loadAlumni();
});

// Role Switcher
function switchRole(role) {
  currentRole = role;
  document.querySelectorAll(".role-btn").forEach(b => {
    b.classList.remove("bg-indigo-600", "text-white", "shadow-md");
    b.classList.add("text-slate-400");
  });

  const activeBtn = document.getElementById(`tab-${role}`);
  if (activeBtn) {
    activeBtn.classList.remove("text-slate-400");
    activeBtn.classList.add("bg-indigo-600", "text-white", "shadow-md");
  }

  document.getElementById("section-student").classList.add("hidden");
  document.getElementById("section-recruiter").classList.add("hidden");
  document.getElementById("section-tpo").classList.add("hidden");

  document.getElementById(`section-${role}`).classList.remove("hidden");

  if (role === "recruiter") {
    runReversePitchSearch();
  } else if (role === "tpo") {
    loadTPOAnalytics();
  }

  if (window.lucide) lucide.createIcons();
}

// Load Students & Drives into Select dropdowns
async function loadInitialData() {
  try {
    const [studentsRes, drivesRes] = await Promise.all([
      fetch("/api/students"),
      fetch("/api/drives")
    ]);
    const students = await studentsRes.json();
    const drives = await drivesRes.json();

    const studentSelect = document.getElementById("diag-student-select");
    studentSelect.innerHTML = students.map(s => `
      <option value="${s.id}">${s.name} (${s.department} • CGPA ${s.cgpa})</option>
    `).join("");

    const companySelect = document.getElementById("diag-company-select");
    companySelect.innerHTML = drives.map(d => `
      <option value="${d.id}">${d.company_name} - ${d.role_title} (${d.ctc_lpa} LPA)</option>
    `).join("");

  } catch (err) {
    console.error("Failed to load initial seed data:", err);
  }
}

// 1. Smart Alerts
async function loadAlerts(studentId) {
  try {
    const res = await fetch(`/api/alerts/student/${studentId}`);
    const alerts = await res.json();
    const container = document.getElementById("alerts-container");

    container.innerHTML = alerts.map(a => `
      <div class="bg-slate-900/90 border border-slate-800 p-4 rounded-xl flex items-start space-x-3 shadow-md hover:border-slate-700 transition-all">
        <div class="mt-0.5 p-2 rounded-lg ${a.urgency === 'high' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20'}">
          <i data-lucide="${a.urgency === 'high' ? 'alert-circle' : 'sparkles'}" class="w-4 h-4"></i>
        </div>
        <div class="flex-1">
          <h4 class="text-sm font-semibold text-white">${a.title}</h4>
          <p class="text-xs text-slate-400 mt-1">${a.message}</p>
        </div>
      </div>
    `).join("");

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Alerts error:", err);
  }
}

// 2. Run Diagnostic Gap Check & Free Resources
async function runDiagnosticCheck() {
  const studentId = document.getElementById("diag-student-select").value;
  const companyId = document.getElementById("diag-company-select").value;

  try {
    const res = await fetch("/api/diagnostics/check-eligibility", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ student_id: parseInt(studentId), company_id: parseInt(companyId) })
    });

    const data = await res.json();
    const diag = data.diagnosis;

    // Badge
    const badge = document.getElementById("eligibility-badge");
    badge.innerText = diag.eligibility_status;
    badge.className = `px-3 py-1 rounded-full text-xs font-semibold ${
      diag.is_eligible 
        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' 
        : (diag.eligibility_status === 'Borderline' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30')
    }`;

    // Gaps
    const gapsContainer = document.getElementById("gaps-container");
    if (diag.gaps_found.length === 0) {
      gapsContainer.innerHTML = `
        <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-emerald-300 text-sm flex items-center space-x-2">
          <i data-lucide="check-circle" class="w-5 h-5"></i>
          <span>All eligibility criteria met! You are fully qualified to register for this campus drive.</span>
        </div>
      `;
    } else {
      gapsContainer.innerHTML = diag.gaps_found.map(g => `
        <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/80 flex items-start justify-between">
          <div class="space-y-1">
            <div class="flex items-center space-x-2">
              <span class="text-xs px-2 py-0.5 rounded font-semibold ${g.severity === 'Critical' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'}">${g.category}</span>
              <span class="text-xs text-slate-400">Required: <strong class="text-slate-200">${g.required}</strong> | Current: <span class="text-rose-400 font-medium">${g.current}</span></span>
            </div>
            <p class="text-xs text-slate-300">${g.remediation}</p>
          </div>
        </div>
      `).join("");
    }

    // Free Resources
    const resSection = document.getElementById("resources-section");
    const resContainer = document.getElementById("resources-container");
    if (diag.curated_free_resources && diag.curated_free_resources.length > 0) {
      resSection.classList.remove("hidden");
      resContainer.innerHTML = diag.curated_free_resources.map(r => `
        <a href="${r.url}" target="_blank" class="p-3.5 bg-slate-800/80 hover:bg-slate-800 border border-slate-700 rounded-xl transition-all group block space-y-1">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-indigo-400 uppercase tracking-wider">${r.skill}</span>
            <span class="text-[11px] text-slate-400">${r.type} • ~${r.est_hours}h</span>
          </div>
          <div class="text-sm font-medium text-white group-hover:text-indigo-300 transition-colors flex items-center gap-1">
            <span>${r.title}</span>
            <i data-lucide="external-link" class="w-3.5 h-3.5 opacity-60"></i>
          </div>
          <p class="text-xs text-slate-400 line-clamp-2">${r.description}</p>
        </a>
      `).join("");
    } else {
      resSection.classList.add("hidden");
    }

    // 4-Week Level-Up Plan
    const planSection = document.getElementById("roadmap-section");
    const planContainer = document.getElementById("roadmap-container");
    if (diag.level_up_plan && diag.level_up_plan.roadmap) {
      planSection.classList.remove("hidden");
      planContainer.innerHTML = diag.level_up_plan.roadmap.map(w => `
        <div class="p-4 rounded-xl bg-slate-800/70 border border-slate-700/70 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">WEEK ${w.week}</span>
            <span class="text-xs text-slate-400 font-medium">${w.theme}</span>
          </div>
          <p class="text-xs font-medium text-slate-200">${w.focus}</p>
          <ul class="text-xs text-slate-400 space-y-1 list-disc list-inside">
            ${w.tasks.map(t => `<li>${t}</li>`).join("")}
          </ul>
          <div class="pt-2 border-t border-slate-700/50 text-[11px] text-emerald-300 font-medium">
            🎯 Milestone: ${w.milestone}
          </div>
        </div>
      `).join("");
    } else {
      planSection.classList.add("hidden");
    }

    if (window.lucide) lucide.createIcons();

  } catch (err) {
    console.error("Diagnostic error:", err);
  }
}

// 3. GitHub Project Authenticity Audit
async function runGitHubAudit() {
  const user = document.getElementById("github-user-input").value || "candidate-portfolio";
  const repo = document.getElementById("github-repo-input").value || "smart-placement-system";
  const studentId = document.getElementById("diag-student-select").value || 1;

  try {
    const res = await fetch("/api/github/audit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: parseInt(studentId),
        github_username: user,
        sample_repo_url: repo
      })
    });

    const data = await res.json();
    const audit = data.audit;

    const container = document.getElementById("github-results-container");
    container.classList.remove("hidden");

    container.innerHTML = `
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 rounded-xl bg-slate-950/80 border border-slate-800">
        <div class="space-y-1">
          <span class="text-xs text-slate-400 uppercase font-semibold">Proof-of-Work Score</span>
          <div class="text-3xl font-bold ${audit.proof_of_work_score >= 75 ? 'text-emerald-400' : 'text-amber-400'}">${audit.proof_of_work_score}/100</div>
          <span class="text-xs ${audit.verified_project_badge ? 'text-emerald-400' : 'text-slate-400'}">
            ${audit.verified_project_badge ? '🛡️ Verified Project Badge Awarded' : '⚠️ Unverified Project'}
          </span>
        </div>
        <div class="md:col-span-3 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-sm font-semibold text-white">${audit.verdict}</span>
            <span class="text-xs px-2 py-0.5 rounded ${audit.is_tutorial_clone ? 'bg-rose-500/20 text-rose-300' : 'bg-emerald-500/20 text-emerald-300'} font-medium">
              ${audit.is_tutorial_clone ? 'Clone Template Detected' : 'Original Custom Architecture'}
            </span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            ${audit.score_breakdown.map(b => `
              <div class="p-2 bg-slate-900 border border-slate-800 rounded-lg">
                <div class="font-medium text-slate-300">${b.factor}: <strong class="text-white">${b.score}/${b.max}</strong></div>
                <div class="text-[11px] text-slate-400">${b.status}</div>
              </div>
            `).join("")}
          </div>
        </div>
      </div>
    `;

    if (window.lucide) lucide.createIcons();

  } catch (err) {
    console.error("GitHub audit error:", err);
  }
}

// 4. Mock Interview Coach
async function generateMockQuestion() {
  const company = document.getElementById("mock-company-select").value;
  const category = document.getElementById("mock-cat-select").value;
  const studentId = document.getElementById("diag-student-select").value || 1;

  try {
    const res = await fetch("/api/mock-interview/generate-question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: parseInt(studentId),
        company_name: company,
        role: "Software Engineer",
        category: category
      })
    });

    const data = await res.json();
    activeSessionId = data.session_id;

    const qBox = document.getElementById("mock-q-box");
    qBox.classList.remove("hidden");
    document.getElementById("mock-q-text").innerText = `🎯 ${data.question}`;
    document.getElementById("mock-feedback-box").classList.add("hidden");
    document.getElementById("mock-answer-input").value = "";

  } catch (err) {
    console.error("Mock Question error:", err);
  }
}

async function submitMockAnswer() {
  if (!activeSessionId) return;
  const answer = document.getElementById("mock-answer-input").value;

  try {
    const res = await fetch("/api/mock-interview/submit-answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: activeSessionId,
        student_answer: answer
      })
    });

    const data = await res.json();
    const fbBox = document.getElementById("mock-feedback-box");
    fbBox.classList.remove("hidden");

    fbBox.innerHTML = `
      <div class="flex items-center justify-between border-b border-slate-800 pb-2">
        <span class="text-sm font-semibold text-white">AI Evaluation Score: <strong class="${data.score >= 70 ? 'text-emerald-400' : 'text-amber-400'}">${data.score}/100</strong></span>
        <span class="text-xs text-slate-400">STAR Evaluator</span>
      </div>
      <div class="space-y-1 text-xs">
        <div class="text-emerald-400 font-medium">✓ Strengths:</div>
        <ul class="list-disc list-inside text-slate-300">
          ${data.strengths.map(s => `<li>${s}</li>`).join("")}
        </ul>
      </div>
      <div class="space-y-1 text-xs">
        <div class="text-amber-400 font-medium">⚡ Key Critique & Areas to Improve:</div>
        <ul class="list-disc list-inside text-slate-300">
          ${data.critique.map(c => `<li>${c}</li>`).join("")}
        </ul>
      </div>
      <div class="pt-2 border-t border-slate-800 text-xs">
        <span class="font-semibold text-indigo-300">💡 Model Answer Guide:</span>
        <p class="text-slate-300 mt-1 italic">${data.model_answer}</p>
      </div>
    `;

  } catch (err) {
    console.error("Mock answer error:", err);
  }
}

// 5. Alumni Directory & Booking
async function loadAlumni() {
  try {
    const res = await fetch("/api/alumni");
    const alumni = await res.json();
    const container = document.getElementById("alumni-cards-container");

    container.innerHTML = alumni.map(a => `
      <div class="p-3.5 bg-slate-800/80 border border-slate-700 rounded-xl flex items-center justify-between shadow-sm">
        <div class="space-y-0.5">
          <div class="flex items-center space-x-2">
            <span class="text-sm font-semibold text-white">${a.name}</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">${a.current_company}</span>
          </div>
          <p class="text-xs text-slate-400">${a.current_role} • Class of ${a.graduation_batch} (${a.department})</p>
        </div>
        <button onclick="requestAlumniSession(${a.id}, '${a.name}')" class="px-3 py-1.5 bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 rounded-lg text-xs font-medium transition-all">
          Connect
        </button>
      </div>
    `).join("");

  } catch (err) {
    console.error("Alumni load error:", err);
  }
}

async function requestAlumniSession(alumniId, name) {
  const studentId = document.getElementById("diag-student-select").value || 1;
  try {
    const res = await fetch("/api/alumni/request-session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: parseInt(studentId),
        alumni_id: alumniId,
        session_type: "15-Min Prep Call"
      })
    });
    const data = await res.json();
    alert(`🎉 Success: ${data.message}\n${data.calendar_invite}`);
  } catch (err) {
    console.error("Booking error:", err);
  }
}

// 6. Recruiter Reverse Pitch Search
async function runReversePitchSearch() {
  const minCgpa = parseFloat(document.getElementById("recruiter-cgpa").value) || 0;
  const dept = document.getElementById("recruiter-dept").value;
  const verifiedOnly = document.getElementById("recruiter-verified-only").checked;

  try {
    const res = await fetch("/api/recruiter/reverse-pitch/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        min_cgpa: minCgpa,
        department: dept || null,
        verified_project_only: verifiedOnly
      })
    });

    const data = await res.json();
    document.getElementById("candidate-count-badge").innerText = `${data.total_matches} candidate(s)`;

    const grid = document.getElementById("candidates-grid");
    grid.innerHTML = data.candidates.map(c => `
      <div class="bg-slate-800/80 border border-slate-700/80 p-4 rounded-xl space-y-3 shadow-md hover:border-slate-600 transition-all">
        <div class="flex items-center justify-between">
          <div class="font-semibold text-white text-sm">${c.name}</div>
          <span class="text-xs px-2 py-0.5 rounded font-medium ${c.verified_project_badge ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-700 text-slate-400'}">
            ${c.verified_project_badge ? '🛡️ Verified' : 'Unverified'}
          </span>
        </div>
        <div class="text-xs text-slate-400 space-y-0.5">
          <div>Dept: <strong class="text-slate-300">${c.department}</strong> | CGPA: <strong class="text-indigo-400">${c.cgpa}</strong></div>
          <div>Skills: <span class="text-slate-300">${c.skills}</span></div>
          ${c.github_username ? `<div>GitHub Proof: <strong class="text-emerald-400">${c.github_proof_score}/100</strong></div>` : ''}
        </div>
        <button onclick="sendFastTrackInvite(${c.id}, '${c.name}')" class="w-full bg-cyan-600/90 hover:bg-cyan-600 text-white font-medium py-1.5 rounded-lg text-xs transition-all shadow-md shadow-cyan-600/20">
          Fast-Track Interview Invite
        </button>
      </div>
    `).join("");

  } catch (err) {
    console.error("Recruiter search error:", err);
  }
}

async function sendFastTrackInvite(studentId, name) {
  try {
    const res = await fetch("/api/recruiter/reverse-pitch/invite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        drive_id: 1, // Amazon or default drive
        student_ids: [studentId],
        custom_message: "You have been fast-tracked for technical rounds based on your verified code portfolio."
      })
    });
    const data = await res.json();
    alert(`🚀 Fast-Track Invite Sent to ${name}!\nStatus: Advanced directly to Online Assessment.`);
  } catch (err) {
    console.error("Invite error:", err);
  }
}

// 7. TPO Placement Analytics
async function loadTPOAnalytics() {
  try {
    const res = await fetch("/api/analytics/tpo-dashboard");
    const data = await res.json();
    const kpis = data.kpis;

    const kpiGrid = document.getElementById("tpo-kpi-grid");
    kpiGrid.innerHTML = `
      <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
        <span class="text-xs text-slate-400 uppercase font-semibold">Total Batch Size</span>
        <div class="text-2xl font-bold text-white">${kpis.total_students} Students</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
        <span class="text-xs text-slate-400 uppercase font-semibold">Placement Rate</span>
        <div class="text-2xl font-bold text-emerald-400">${kpis.placement_rate_pct}%</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
        <span class="text-xs text-slate-400 uppercase font-semibold">Average CTC</span>
        <div class="text-2xl font-bold text-indigo-400">${kpis.average_ctc_lpa} LPA</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
        <span class="text-xs text-slate-400 uppercase font-semibold">At-Risk Students</span>
        <div class="text-2xl font-bold text-rose-400">${kpis.at_risk_students_count}</div>
      </div>
    `;

    // At-Risk Table
    const tbody = document.getElementById("tpo-at-risk-tbody");
    tbody.innerHTML = data.at_risk_students.map(s => `
      <tr class="hover:bg-slate-800/40 transition-colors">
        <td class="px-4 py-3 font-medium text-white">${s.name}</td>
        <td class="px-4 py-3 text-slate-400">${s.roll_no}</td>
        <td class="px-4 py-3 text-slate-300">${s.department}</td>
        <td class="px-4 py-3 font-semibold text-rose-400">${s.cgpa}</td>
        <td class="px-4 py-3 text-rose-400 font-semibold">${s.backlogs}</td>
        <td class="px-4 py-3"><span class="px-2 py-0.5 rounded text-xs font-semibold bg-rose-500/20 text-rose-300">At-Risk</span></td>
        <td class="px-4 py-3">
          <button onclick="alert('Student ${s.name} successfully enrolled into ${s.suggested_cohort}!')" class="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-xs font-medium transition-all">
            Assign to ${s.suggested_cohort}
          </button>
        </td>
      </tr>
    `).join("");

    // Cohorts
    const cohortsGrid = document.getElementById("cohorts-grid");
    cohortsGrid.innerHTML = data.active_cohorts.map(c => `
      <div class="p-4 bg-slate-800/80 border border-slate-700 rounded-xl space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-sm font-semibold text-white">${c.name}</span>
          <span class="text-xs px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">${c.category}</span>
        </div>
        <p class="text-xs text-slate-400">Mentor: <strong class="text-slate-300">${c.mentor}</strong></p>
        <p class="text-xs text-slate-300 bg-slate-900/60 p-2 rounded-lg border border-slate-800 font-mono">Task: ${c.weekly_task}</p>
      </div>
    `).join("");

  } catch (err) {
    console.error("TPO load error:", err);
  }
}
