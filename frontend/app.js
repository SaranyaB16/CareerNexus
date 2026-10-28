// CareerNexus Client Engine
let currentRole = "student";
let activeSessionId = null;
let currentUser = null;
let currentPersona = "student";
let currentPersonaStep = 1;

let gatewayRole = "student";   // "student" or "recruiter"
let gatewayMode = "login";     // "login" or "signup"
let sidebarOpen = false;

// Step metadata for dynamic breadcrumbs
const personaStepLabels = {
  student: {
    1: "Student Step 1: Placement Alerts",
    2: "Student Step 2: Gap Diagnostic",
    3: "Student Step 3: GitHub Authenticity",
    4: "Student Step 4: AI Mock Coach",
    5: "Student Step 5: Alumni Referral Bridge"
  },
  recruiter: {
    1: "Recruiter Module 1: Talent Sourcing",
    2: "Recruiter Module 2: Code Proof Inspector",
    3: "Recruiter Module 3: Interview Shortlist",
    4: "Recruiter Module 4: Drive Forensics"
  },
  tpo: {
    1: "TPO Module 1: Placement KPIs",
    2: "TPO Module 2: Early-Warning Radar",
    3: "TPO Module 3: Remediation Cohorts"
  }
};

// Initialize when page loads
document.addEventListener("DOMContentLoaded", async () => {
  if (window.lucide) lucide.createIcons();
  
  // Check for saved session
  const savedUser = localStorage.getItem("careernexus_user");
  if (savedUser) {
    try {
      currentUser = JSON.parse(savedUser);
      enterDashboard(currentUser);
    } catch(e) {
      showGatewayPage();
    }
  } else {
    showGatewayPage();
  }

  await loadInitialData();
  await loadAlerts(currentUser?.student_id || 1);
  await loadAlumni();
});

// ==================== PAGE 1 <-> PAGE 2 FLOW ====================

function showGatewayPage() {
  document.getElementById("page-1-gateway").classList.remove("hidden");
  document.getElementById("page-2-dashboard").classList.add("hidden");
  document.getElementById("page-1-indicator").classList.remove("hidden");
  document.getElementById("page-2-nav").classList.add("hidden");
  document.getElementById("sidebar-toggle-btn").classList.add("hidden");
  document.getElementById("step-breadcrumb").classList.add("hidden");
  if (window.lucide) lucide.createIcons();
}

function enterDashboard(user) {
  document.getElementById("page-1-gateway").classList.add("hidden");
  document.getElementById("page-2-dashboard").classList.remove("hidden");
  document.getElementById("page-1-indicator").classList.add("hidden");
  document.getElementById("page-2-nav").classList.remove("hidden");
  document.getElementById("sidebar-toggle-btn").classList.remove("hidden");
  document.getElementById("step-breadcrumb").classList.remove("hidden");

  if (user && user.role === "recruiter") {
    switchRole("recruiter");
  } else {
    switchRole("student");
  }

  if (window.lucide) lucide.createIcons();
}

function handleLogoClick() {
  if (currentUser) {
    switchRole(currentUser.role === "recruiter" ? "recruiter" : "student");
  } else {
    showGatewayPage();
  }
}

function logout() {
  currentUser = null;
  localStorage.removeItem("careernexus_user");
  showGatewayPage();
  document.getElementById("gate-email").value = "";
  document.getElementById("gate-password").value = "";
  document.getElementById("gate-error-msg").classList.add("hidden");
}

// ==================== PERSONA ROLE SWITCHER (DYNAMIC SIDEBAR) ====================

function switchRole(role) {
  currentRole = role;
  currentPersona = role;

  // 1. Update top persona buttons
  const tabStudent = document.getElementById("tab-student");
  const tabRecruiter = document.getElementById("tab-recruiter");
  const tabTpo = document.getElementById("tab-tpo");

  [tabStudent, tabRecruiter, tabTpo].forEach(btn => {
    if (btn) btn.className = "role-btn px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1.5 text-slate-400 hover:text-white";
  });

  if (role === "student" && tabStudent) {
    tabStudent.className = "role-btn px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1.5 bg-emerald-500 text-slate-950 shadow-md";
  } else if (role === "recruiter" && tabRecruiter) {
    tabRecruiter.className = "role-btn px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1.5 bg-cyan-500 text-slate-950 shadow-md";
  } else if (role === "tpo" && tabTpo) {
    tabTpo.className = "role-btn px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1.5 bg-indigo-500 text-white shadow-md";
  }

  // 2. Switch Left Sidebar Navigation according to selected Persona
  const navStudent = document.getElementById("sidebar-nav-student");
  const navRecruiter = document.getElementById("sidebar-nav-recruiter");
  const navTpo = document.getElementById("sidebar-nav-tpo");

  const headerTitle = document.getElementById("sidebar-header-title");
  const headerBadge = document.getElementById("sidebar-header-badge");
  const headerIcon = document.getElementById("sidebar-header-icon");
  const headerIconBox = document.getElementById("sidebar-header-icon-box");

  if (role === "student") {
    if (navStudent) navStudent.classList.remove("hidden");
    if (navRecruiter) navRecruiter.classList.add("hidden");
    if (navTpo) navTpo.classList.add("hidden");

    if (headerTitle) headerTitle.innerText = "Student Portal";
    if (headerBadge) {
      headerBadge.innerText = "5 Steps";
      headerBadge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30";
    }
    if (headerIcon) headerIcon.setAttribute("data-lucide", "graduation-cap");
    if (headerIconBox) headerIconBox.className = "w-6 h-6 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400";

    updateSidebarProfile("student");
    navigateToPersonaStep("student", 1);

  } else if (role === "recruiter") {
    if (navStudent) navStudent.classList.add("hidden");
    if (navRecruiter) navRecruiter.classList.remove("hidden");
    if (navTpo) navTpo.classList.add("hidden");

    if (headerTitle) headerTitle.innerText = "Recruiter Desk";
    if (headerBadge) {
      headerBadge.innerText = "4 Modules";
      headerBadge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30";
    }
    if (headerIcon) headerIcon.setAttribute("data-lucide", "briefcase");
    if (headerIconBox) headerIconBox.className = "w-6 h-6 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400";

    updateSidebarProfile("recruiter");
    navigateToPersonaStep("recruiter", 1);
    runReversePitchSearch();

  } else if (role === "tpo") {
    if (navStudent) navStudent.classList.add("hidden");
    if (navRecruiter) navRecruiter.classList.add("hidden");
    if (navTpo) navTpo.classList.remove("hidden");

    if (headerTitle) headerTitle.innerText = "TPO Command Center";
    if (headerBadge) {
      headerBadge.innerText = "3 Modules";
      headerBadge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/30";
    }
    if (headerIcon) headerIcon.setAttribute("data-lucide", "shield-check");
    if (headerIconBox) headerIconBox.className = "w-6 h-6 rounded-lg bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400";

    updateSidebarProfile("tpo");
    navigateToPersonaStep("tpo", 1);
    loadTPOAnalytics();
  }

  if (window.lucide) lucide.createIcons();
}

function updateSidebarProfile(role) {
  const avatar = document.getElementById("user-avatar");
  const nameLabel = document.getElementById("user-name");
  const roleBadge = document.getElementById("user-role-badge");

  const sideAvatar = document.getElementById("sidebar-user-avatar");
  const sideName = document.getElementById("sidebar-user-name");
  const sideRole = document.getElementById("sidebar-user-role");
  const sideSwitch = document.getElementById("sidebar-switch-label");

  if (role === "student") {
    const sName = currentUser && currentUser.role === "student" ? currentUser.name : "Aarav Sharma";
    const sDept = currentUser && currentUser.role === "student" ? (currentUser.department || "Computer Science") : "Computer Science (8.4 CGPA)";
    
    if (avatar) {
      avatar.innerText = "A";
      avatar.className = "w-6 h-6 rounded-lg font-bold text-xs flex items-center justify-center bg-emerald-500 text-slate-950";
    }
    if (nameLabel) nameLabel.innerText = sName;
    if (roleBadge) {
      roleBadge.innerText = "Student";
      roleBadge.className = "text-[10px] text-emerald-400 font-medium capitalize";
    }

    if (sideAvatar) {
      sideAvatar.innerText = "A";
      sideAvatar.className = "w-8 h-8 rounded-lg bg-emerald-500 text-slate-950 font-extrabold text-sm flex items-center justify-center flex-shrink-0";
    }
    if (sideName) sideName.innerText = sName;
    if (sideRole) {
      sideRole.innerText = sDept;
      sideRole.className = "text-[10px] text-emerald-400 font-medium truncate";
    }
    if (sideSwitch) sideSwitch.innerText = "Switch to Recruiter Desk";

  } else if (role === "recruiter") {
    const rCompany = currentUser && currentUser.role === "recruiter" ? (currentUser.company || "Amazon") : "Amazon";
    const rName = currentUser && currentUser.role === "recruiter" ? currentUser.name : "Amazon Hiring Team";

    if (avatar) {
      avatar.innerText = "R";
      avatar.className = "w-6 h-6 rounded-lg font-bold text-xs flex items-center justify-center bg-cyan-500 text-slate-950";
    }
    if (nameLabel) nameLabel.innerText = rName;
    if (roleBadge) {
      roleBadge.innerText = `${rCompany} Recruiter`;
      roleBadge.className = "text-[10px] text-cyan-400 font-medium capitalize";
    }

    if (sideAvatar) {
      sideAvatar.innerText = "R";
      sideAvatar.className = "w-8 h-8 rounded-lg bg-cyan-500 text-slate-950 font-extrabold text-sm flex items-center justify-center flex-shrink-0";
    }
    if (sideName) sideName.innerText = rName;
    if (sideRole) {
      sideRole.innerText = `${rCompany} (Talent Partner)`;
      sideRole.className = "text-[10px] text-cyan-400 font-medium truncate";
    }
    if (sideSwitch) sideSwitch.innerText = "Switch to Student Portal";

  } else if (role === "tpo") {
    if (avatar) {
      avatar.innerText = "T";
      avatar.className = "w-6 h-6 rounded-lg font-bold text-xs flex items-center justify-center bg-indigo-500 text-white";
    }
    if (nameLabel) nameLabel.innerText = "Placement Officer";
    if (roleBadge) {
      roleBadge.innerText = "TPO Cell Admin";
      roleBadge.className = "text-[10px] text-indigo-400 font-medium capitalize";
    }

    if (sideAvatar) {
      sideAvatar.innerText = "T";
      sideAvatar.className = "w-8 h-8 rounded-lg bg-indigo-500 text-white font-extrabold text-sm flex items-center justify-center flex-shrink-0";
    }
    if (sideName) sideName.innerText = "Campus TPO Cell";
    if (sideRole) {
      sideRole.innerText = "Placement Administration";
      sideRole.className = "text-[10px] text-indigo-400 font-medium truncate";
    }
    if (sideSwitch) sideSwitch.innerText = "Switch to Student Portal";
  }
}

function quickRoleSwitch() {
  if (currentRole === "student") {
    switchRole("recruiter");
  } else {
    switchRole("student");
  }
}

// ==================== STEP-BY-STEP PAGE NAVIGATION ====================

function navigateToPersonaStep(persona, step) {
  currentPersona = persona;
  currentPersonaStep = parseInt(step) || 1;

  // Max steps per persona
  const maxSteps = { student: 5, recruiter: 4, tpo: 3 };
  const max = maxSteps[persona] || 5;
  if (currentPersonaStep < 1) currentPersonaStep = 1;
  if (currentPersonaStep > max) currentPersonaStep = max;

  // 1. Hide ALL pages across ALL personas
  const allPageIds = [
    "page-student-1", "page-student-2", "page-student-3", "page-student-4", "page-student-5",
    "page-recruiter-1", "page-recruiter-2", "page-recruiter-3", "page-recruiter-4",
    "page-tpo-1", "page-tpo-2", "page-tpo-3"
  ];

  allPageIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add("hidden");
  });

  // 2. Show the targeted page
  const targetPage = document.getElementById(`page-${persona}-${currentPersonaStep}`);
  if (targetPage) {
    targetPage.classList.remove("hidden");
  }

  // 3. Update the active pill in that persona's sidebar navigation
  for (let s = 1; s <= max; s++) {
    const item = document.getElementById(`side-${persona}-item-${s}`);
    if (item) {
      item.classList.remove("active", "active-cyan", "active-indigo");
      const bubble = item.querySelector(".step-num");

      if (s === currentPersonaStep) {
        if (persona === "recruiter") {
          item.classList.add("active-cyan");
          if (bubble) bubble.className = "step-num w-7 h-7 rounded-xl bg-cyan-500 text-slate-950 text-xs font-extrabold flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm";
        } else if (persona === "tpo") {
          item.classList.add("active-indigo");
          if (bubble) bubble.className = "step-num w-7 h-7 rounded-xl bg-indigo-500 text-white text-xs font-extrabold flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm";
        } else {
          item.classList.add("active");
          if (bubble) bubble.className = "step-num w-7 h-7 rounded-xl bg-emerald-500 text-slate-950 text-xs font-extrabold flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm";
        }
      } else {
        if (bubble) bubble.className = "step-num w-7 h-7 rounded-xl bg-slate-800 text-slate-400 text-xs font-extrabold flex items-center justify-center flex-shrink-0 mt-0.5";
      }
    }
  }

  // 4. Update Top Breadcrumb
  const breadcrumb = document.getElementById("breadcrumb-step-label");
  const dot = document.getElementById("breadcrumb-dot");
  if (breadcrumb) {
    breadcrumb.innerText = personaStepLabels[persona]?.[currentPersonaStep] || `${persona} Step ${currentPersonaStep}`;
  }
  if (dot) {
    dot.className = `w-2 h-2 rounded-full animate-pulse ${persona === 'recruiter' ? 'bg-cyan-400' : (persona === 'tpo' ? 'bg-indigo-400' : 'bg-emerald-400')}`;
  }

  // 5. Automatic Data Loading for Specific Modules
  if (persona === "recruiter") {
    if (currentPersonaStep === 1) runReversePitchSearch();
    if (currentPersonaStep === 3) loadRecruiterPipeline();
    if (currentPersonaStep === 4) loadRecruiterDriveForensics();
  } else if (persona === "tpo") {
    loadTPOAnalytics();
  }

  // 6. Smooth Scroll to Top
  const contentArea = document.getElementById("step-content-area");
  if (contentArea) {
    contentArea.scrollTo({ top: 0, behavior: "smooth" });
  }

  // 7. Close Mobile Drawer
  toggleSidebar(false);

  if (window.lucide) lucide.createIcons();
}

function toggleSidebar(forceState) {
  const sidebar = document.getElementById("dashboard-sidebar");
  const backdrop = document.getElementById("sidebar-backdrop");
  if (!sidebar) return;

  if (forceState !== undefined) {
    sidebarOpen = forceState;
  } else {
    sidebarOpen = !sidebarOpen;
  }

  if (sidebarOpen) {
    sidebar.classList.remove("-translate-x-full");
    if (backdrop) backdrop.classList.remove("hidden");
  } else {
    sidebar.classList.add("-translate-x-full");
    if (backdrop) backdrop.classList.add("hidden");
  }
}

// ==================== GATEWAY (PAGE 1) CONTROLS ====================

function selectGatewayRole(role) {
  gatewayRole = role;
  const isStudent = role === "student";

  const btnStudent = document.getElementById("role-btn-student");
  const btnRecruiter = document.getElementById("role-btn-recruiter");
  const checkStudent = document.getElementById("icon-check-student");
  const checkRecruiter = document.getElementById("icon-check-recruiter");
  const submitBtn = document.getElementById("gate-submit-btn");

  if (isStudent) {
    btnStudent.className = "p-4 rounded-2xl border-2 border-emerald-500 bg-emerald-500/10 text-left transition-all relative group shadow-lg shadow-emerald-500/10";
    checkStudent.className = "w-5 h-5 rounded-full bg-emerald-500 text-slate-950 flex items-center justify-center text-xs font-bold";
    checkStudent.innerText = "✓";

    btnRecruiter.className = "p-4 rounded-2xl border-2 border-slate-800 bg-slate-900/60 text-left transition-all relative group hover:border-slate-700";
    checkRecruiter.className = "w-5 h-5 rounded-full bg-slate-800 text-transparent flex items-center justify-center text-xs font-bold";
    checkRecruiter.innerText = "✓";

    submitBtn.className = "w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-3 rounded-xl text-sm transition-all flex items-center justify-center space-x-2 shadow-lg shadow-emerald-500/20";
    submitBtn.querySelector("span").innerText = gatewayMode === "login" ? "Sign In to Student Portal" : "Create Student Account";
  } else {
    btnRecruiter.className = "p-4 rounded-2xl border-2 border-cyan-500 bg-cyan-500/10 text-left transition-all relative group shadow-lg shadow-cyan-500/10";
    checkRecruiter.className = "w-5 h-5 rounded-full bg-cyan-500 text-slate-950 flex items-center justify-center text-xs font-bold";
    checkRecruiter.innerText = "✓";

    btnStudent.className = "p-4 rounded-2xl border-2 border-slate-800 bg-slate-900/60 text-left transition-all relative group hover:border-slate-700";
    checkStudent.className = "w-5 h-5 rounded-full bg-slate-800 text-transparent flex items-center justify-center text-xs font-bold";
    checkStudent.innerText = "✓";

    submitBtn.className = "w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-3 rounded-xl text-sm transition-all flex items-center justify-center space-x-2 shadow-lg shadow-cyan-500/20";
    submitBtn.querySelector("span").innerText = gatewayMode === "login" ? "Sign In to Recruiter Desk" : "Create Recruiter Account";
  }

  updateGatewayExtraFields();
  if (window.lucide) lucide.createIcons();
}

function setGatewayAuthMode(mode) {
  gatewayMode = mode;
  const isLogin = mode === "login";

  const tabLogin = document.getElementById("gate-tab-login");
  const tabSignup = document.getElementById("gate-tab-signup");
  const submitBtn = document.getElementById("gate-submit-btn");

  const activeColor = gatewayRole === "student" ? "bg-emerald-500 text-slate-950 shadow-md" : "bg-cyan-500 text-slate-950 shadow-md";

  if (isLogin) {
    tabLogin.className = `flex-1 py-2 rounded-lg text-xs font-bold ${activeColor} transition-all`;
    tabSignup.className = "flex-1 py-2 rounded-lg text-xs font-bold text-slate-400 hover:text-white transition-all";
    submitBtn.querySelector("span").innerText = gatewayRole === "student" ? "Sign In to Student Portal" : "Sign In to Recruiter Desk";
  } else {
    tabSignup.className = `flex-1 py-2 rounded-lg text-xs font-bold ${activeColor} transition-all`;
    tabLogin.className = "flex-1 py-2 rounded-lg text-xs font-bold text-slate-400 hover:text-white transition-all";
    submitBtn.querySelector("span").innerText = gatewayRole === "student" ? "Create Student Account" : "Create Recruiter Account";
  }

  document.getElementById("gate-field-name").classList.toggle("hidden", isLogin);
  updateGatewayExtraFields();
}

function updateGatewayExtraFields() {
  const isSignup = gatewayMode === "signup";
  document.getElementById("gate-field-student-extras").classList.toggle("hidden", !isSignup || gatewayRole !== "student");
  document.getElementById("gate-field-recruiter-extras").classList.toggle("hidden", !isSignup || gatewayRole !== "recruiter");
}

async function handleGatewayAuth(e) {
  e.preventDefault();
  const errorBox = document.getElementById("gate-error-msg");
  const errorText = document.getElementById("gate-error-text");
  errorBox.classList.add("hidden");

  const email = document.getElementById("gate-email").value.trim();
  const password = document.getElementById("gate-password").value;

  const endpoint = gatewayMode === "login" ? "/api/auth/login" : "/api/auth/signup";

  const payload = {
    email: email,
    password: password,
    role: gatewayRole
  };

  if (gatewayMode === "signup") {
    payload.name = document.getElementById("gate-name").value.trim() || (gatewayRole === "student" ? "Student User" : "Recruiter User");
    if (gatewayRole === "student") {
      payload.department = document.getElementById("gate-dept").value;
      payload.cgpa = parseFloat(document.getElementById("gate-cgpa").value) || 8.0;
    } else {
      payload.company = document.getElementById("gate-company").value.trim() || "Visiting Tech Partner";
    }
  }

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      errorText.innerText = data.detail || "Authentication failed. Please verify credentials.";
      errorBox.classList.remove("hidden");
      return;
    }

    currentUser = data.user;
    localStorage.setItem("careernexus_user", JSON.stringify(currentUser));
    enterDashboard(currentUser);

  } catch (err) {
    errorText.innerText = "Connection error. Please ensure CareerNexus server is running.";
    errorBox.classList.remove("hidden");
  }
}

function fastGatewayLogin(role) {
  if (role === "student") {
    document.getElementById("gate-email").value = "aarav.sharma@college.edu";
    document.getElementById("gate-password").value = "password123";
    selectGatewayRole("student");
  } else {
    document.getElementById("gate-email").value = "recruiter@amazon.com";
    document.getElementById("gate-password").value = "password123";
    selectGatewayRole("recruiter");
  }
  setGatewayAuthMode("login");
  document.getElementById("gateway-auth-form").dispatchEvent(new Event("submit"));
}

// ==================== CORE PLATFORM APIS & DATA ====================

async function loadInitialData() {
  try {
    const [studentsRes, drivesRes] = await Promise.all([
      fetch("/api/students"),
      fetch("/api/drives")
    ]);
    const students = await studentsRes.json();
    const drives = await drivesRes.json();

    // Student Diagnostic Select
    const studentSelect = document.getElementById("diag-student-select");
    if (studentSelect) {
      studentSelect.innerHTML = students.map(s => `
        <option value="${s.id}">${s.name} (${s.department} • CGPA ${s.cgpa})</option>
      `).join("");
    }

    // Company Drive Diagnostic Select
    const companySelect = document.getElementById("diag-company-select");
    if (companySelect) {
      companySelect.innerHTML = drives.map(d => `
        <option value="${d.id}">${d.company_name} - ${d.role_title} (${d.ctc_lpa} LPA)</option>
      `).join("");
    }

    // Recruiter Drive Manager Select
    const recruiterDriveSelect = document.getElementById("recruiter-drive-select");
    if (recruiterDriveSelect) {
      recruiterDriveSelect.innerHTML = drives.map(d => `
        <option value="${d.id}">${d.company_name} - ${d.role_title} (${d.ctc_lpa} LPA)</option>
      `).join("");
    }

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

    if (container) {
      container.innerHTML = alerts.map(a => `
        <div class="bg-slate-900/90 border border-slate-800 p-4 rounded-2xl flex items-start space-x-3.5 shadow-md hover:border-slate-700 transition-all">
          <div class="mt-0.5 p-2 rounded-xl ${a.urgency === 'high' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}">
            <i data-lucide="${a.urgency === 'high' ? 'alert-circle' : 'sparkles'}" class="w-4 h-4"></i>
          </div>
          <div class="flex-1">
            <h4 class="text-sm font-bold text-white">${a.title}</h4>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">${a.message}</p>
          </div>
        </div>
      `).join("");
    }

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
    if (badge) {
      badge.innerText = diag.eligibility_status;
      badge.className = `px-3.5 py-1 rounded-full text-xs font-bold ${
        diag.is_eligible 
          ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' 
          : (diag.eligibility_status === 'Borderline' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30')
      }`;
    }

    // Gaps
    const gapsContainer = document.getElementById("gaps-container");
    if (gapsContainer) {
      if (diag.gaps_found.length === 0) {
        gapsContainer.innerHTML = `
          <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-emerald-300 text-sm flex items-center space-x-2">
            <i data-lucide="check-circle" class="w-5 h-5"></i>
            <span>All eligibility criteria met! You are fully qualified to register for this campus drive.</span>
          </div>
        `;
      } else {
        gapsContainer.innerHTML = diag.gaps_found.map(g => `
          <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex items-start justify-between">
            <div class="space-y-1">
              <div class="flex items-center space-x-2">
                <span class="text-xs px-2.5 py-0.5 rounded font-bold ${g.severity === 'Critical' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'}">${g.category}</span>
                <span class="text-xs text-slate-400">Required: <strong class="text-slate-200">${g.required}</strong> | Current: <span class="text-rose-400 font-semibold">${g.current}</span></span>
              </div>
              <p class="text-xs text-slate-300">${g.remediation}</p>
            </div>
          </div>
        `).join("");
      }
    }

    // Free Resources
    const resSection = document.getElementById("resources-section");
    const resContainer = document.getElementById("resources-container");
    if (diag.curated_free_resources && diag.curated_free_resources.length > 0) {
      if (resSection) resSection.classList.remove("hidden");
      if (resContainer) {
        resContainer.innerHTML = diag.curated_free_resources.map(r => `
          <a href="${r.url}" target="_blank" class="p-4 bg-slate-900 hover:bg-slate-850 border border-slate-800 hover:border-cyan-500/40 rounded-2xl transition-all group block space-y-1.5 shadow-sm">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider">${r.skill}</span>
              <span class="text-[11px] text-slate-400">${r.type} • ~${r.est_hours}h</span>
            </div>
            <div class="text-sm font-semibold text-white group-hover:text-cyan-300 transition-colors flex items-center gap-1.5">
              <span>${r.title}</span>
              <i data-lucide="external-link" class="w-3.5 h-3.5 opacity-60"></i>
            </div>
            <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">${r.description}</p>
          </a>
        `).join("");
      }
    } else {
      if (resSection) resSection.classList.add("hidden");
    }

    // 4-Week Level-Up Plan
    const planSection = document.getElementById("roadmap-section");
    const planContainer = document.getElementById("roadmap-container");
    if (diag.level_up_plan && diag.level_up_plan.roadmap) {
      if (planSection) planSection.classList.remove("hidden");
      if (planContainer) {
        planContainer.innerHTML = diag.level_up_plan.roadmap.map(w => `
          <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-extrabold px-2.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400">WEEK ${w.week}</span>
              <span class="text-xs text-slate-400 font-semibold">${w.theme}</span>
            </div>
            <p class="text-xs font-medium text-slate-200">${w.focus}</p>
            <ul class="text-xs text-slate-400 space-y-1 list-disc list-inside">
              ${w.tasks.map(t => `<li>${t}</li>`).join("")}
            </ul>
            <div class="pt-2 border-t border-slate-800 text-[11px] text-emerald-300 font-semibold">
              🎯 Milestone: ${w.milestone}
            </div>
          </div>
        `).join("");
      }
    } else {
      if (planSection) planSection.classList.add("hidden");
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
  const studentId = document.getElementById("diag-student-select")?.value || 1;

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

    const placeholder = document.getElementById("github-placeholder-prompt");
    if (placeholder) placeholder.classList.add("hidden");

    const container = document.getElementById("github-results-container");
    if (container) {
      container.classList.remove("hidden");
      container.innerHTML = renderGitHubAuditCard(audit);
    }

    if (window.lucide) lucide.createIcons();

  } catch (err) {
    console.error("GitHub audit error:", err);
  }
}

function renderGitHubAuditCard(audit) {
  return `
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-5 rounded-2xl bg-slate-950 border border-slate-800">
      <div class="space-y-1">
        <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Proof-of-Work Score</span>
        <div class="text-3xl font-extrabold ${audit.proof_of_work_score >= 75 ? 'text-emerald-400' : 'text-amber-400'}">${audit.proof_of_work_score}/100</div>
        <span class="text-xs font-semibold ${audit.verified_project_badge ? 'text-emerald-400' : 'text-slate-400'}">
          ${audit.verified_project_badge ? '🛡️ Verified Project Badge Awarded' : '⚠️ Unverified Project'}
        </span>
      </div>
      <div class="md:col-span-3 space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-sm font-bold text-white">${audit.verdict}</span>
          <span class="text-xs px-2.5 py-0.5 rounded font-semibold ${audit.is_tutorial_clone ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'}">
            ${audit.is_tutorial_clone ? 'Clone Template Detected' : 'Original Custom Architecture'}
          </span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
          ${audit.score_breakdown.map(b => `
            <div class="p-2.5 bg-slate-900 border border-slate-800 rounded-xl">
              <div class="font-semibold text-slate-300">${b.factor}: <strong class="text-white">${b.score}/${b.max}</strong></div>
              <div class="text-[11px] text-slate-400">${b.status}</div>
            </div>
          `).join("")}
        </div>
      </div>
    </div>
  `;
}

// 4. Recruiter Code Proof Inspector
async function runRecruiterGitHubAudit() {
  const user = document.getElementById("recruiter-github-user").value || "aarav-dev";
  const repo = document.getElementById("recruiter-github-repo").value || "careernexus-core";

  try {
    const res = await fetch("/api/github/audit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: 1,
        github_username: user,
        sample_repo_url: repo
      })
    });

    const data = await res.json();
    const audit = data.audit;

    const placeholder = document.getElementById("recruiter-github-placeholder");
    if (placeholder) placeholder.classList.add("hidden");

    const container = document.getElementById("recruiter-github-results");
    if (container) {
      container.classList.remove("hidden");
      container.innerHTML = renderGitHubAuditCard(audit);
    }

    if (window.lucide) lucide.createIcons();

  } catch (err) {
    console.error("Recruiter code audit error:", err);
  }
}

// 5. AI Mock Interview Coach
async function generateMockQuestion() {
  const company = document.getElementById("mock-company-select").value;
  const category = document.getElementById("mock-cat-select").value;
  const studentId = document.getElementById("diag-student-select")?.value || 1;

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
    if (qBox) qBox.classList.remove("hidden");
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
    if (fbBox) {
      fbBox.classList.remove("hidden");

      fbBox.innerHTML = `
        <div class="flex items-center justify-between border-b border-slate-800 pb-2">
          <span class="text-sm font-bold text-white">AI Evaluation Score: <strong class="${data.score >= 70 ? 'text-emerald-400' : 'text-amber-400'}">${data.score}/100</strong></span>
          <span class="text-xs text-slate-400">STAR Evaluator</span>
        </div>
        <div class="space-y-1 text-xs">
          <div class="text-emerald-400 font-bold">✓ Strengths:</div>
          <ul class="list-disc list-inside text-slate-300">
            ${data.strengths.map(s => `<li>${s}</li>`).join("")}
          </ul>
        </div>
        <div class="space-y-1 text-xs">
          <div class="text-amber-400 font-bold">⚡ Key Critique & Areas to Improve:</div>
          <ul class="list-disc list-inside text-slate-300">
            ${data.critique.map(c => `<li>${c}</li>`).join("")}
          </ul>
        </div>
        <div class="pt-2 border-t border-slate-800 text-xs">
          <span class="font-bold text-cyan-300">💡 Model Answer Guide:</span>
          <p class="text-slate-300 mt-1 italic">${data.model_answer}</p>
        </div>
      `;
    }

  } catch (err) {
    console.error("Mock answer error:", err);
  }
}

// 6. Alumni Directory & Booking
async function loadAlumni() {
  try {
    const res = await fetch("/api/alumni");
    const alumni = await res.json();
    const container = document.getElementById("alumni-cards-container");

    if (container) {
      container.innerHTML = alumni.map(a => `
        <div class="p-4 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-between shadow-sm">
          <div class="space-y-0.5">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-bold text-white">${a.name}</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 font-semibold">${a.current_company}</span>
            </div>
            <p class="text-xs text-slate-400">${a.current_role} • Class of ${a.graduation_batch} (${a.department})</p>
          </div>
          <button onclick="requestAlumniSession(${a.id}, '${a.name}')" class="px-3.5 py-1.5 bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/30 rounded-xl text-xs font-bold transition-all">
            Connect
          </button>
        </div>
      `).join("");
    }

  } catch (err) {
    console.error("Alumni load error:", err);
  }
}

async function requestAlumniSession(alumniId, name) {
  const studentId = document.getElementById("diag-student-select")?.value || 1;
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

// 7. Recruiter Reverse Pitch Search
async function runReversePitchSearch() {
  const cgpaInput = document.getElementById("recruiter-cgpa");
  const deptInput = document.getElementById("recruiter-dept");
  const verifiedInput = document.getElementById("recruiter-verified-only");

  const minCgpa = cgpaInput ? parseFloat(cgpaInput.value) || 0 : 0;
  const dept = deptInput ? deptInput.value : "";
  const verifiedOnly = verifiedInput ? verifiedInput.checked : false;

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
    const countBadge = document.getElementById("candidate-count-badge");
    if (countBadge) countBadge.innerText = `${data.total_matches} candidate(s)`;

    const grid = document.getElementById("candidates-grid");
    if (grid) {
      grid.innerHTML = data.candidates.map(c => `
        <div class="glass-card p-5 rounded-2xl space-y-3 shadow-md hover:border-cyan-500/30 transition-all">
          <div class="flex items-center justify-between">
            <div class="font-bold text-white text-sm">${c.name}</div>
            <span class="text-xs px-2.5 py-0.5 rounded font-semibold ${c.verified_project_badge ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-800 text-slate-400'}">
              ${c.verified_project_badge ? '🛡️ Verified' : 'Unverified'}
            </span>
          </div>
          <div class="text-xs text-slate-400 space-y-1">
            <div>Dept: <strong class="text-slate-200">${c.department}</strong> | CGPA: <strong class="text-cyan-400">${c.cgpa}</strong></div>
            <div>Skills: <span class="text-slate-300">${c.skills}</span></div>
            ${c.github_username ? `<div>GitHub Proof: <strong class="text-emerald-400">${c.github_proof_score}/100</strong></div>` : ''}
          </div>
          <button onclick="sendFastTrackInvite(${c.id}, '${c.name}')" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-2 rounded-xl text-xs transition-all shadow-md shadow-cyan-500/15">
            Fast-Track Interview Invite
          </button>
        </div>
      `).join("");
    }

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
        drive_id: 1, // Amazon SDE-1
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

// 8. Recruiter Pipeline Tracker
async function loadRecruiterPipeline() {
  const tbody = document.getElementById("recruiter-pipeline-tbody");
  if (!tbody) return;

  try {
    const res = await fetch("/api/students");
    const students = await res.json();

    tbody.innerHTML = students.map((s, idx) => {
      const stages = ["Invited (Fast-Track)", "Online Assessment", "Technical Round 1", "Offered"];
      const currentStage = stages[idx % stages.length];
      const stageColor = currentStage === "Offered" 
        ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"
        : (currentStage === "Technical Round 1" ? "bg-cyan-500/20 text-cyan-300 border-cyan-500/30" : "bg-amber-500/20 text-amber-300 border-amber-500/30");

      return `
        <tr class="hover:bg-slate-900/60 transition-colors">
          <td class="px-4 py-3.5 font-bold text-white">${s.name}</td>
          <td class="px-4 py-3.5 text-slate-300">${s.department}</td>
          <td class="px-4 py-3.5 font-bold text-cyan-400">${s.cgpa}</td>
          <td class="px-4 py-3.5 font-mono text-emerald-400 font-bold">${s.github_proof_score}/100</td>
          <td class="px-4 py-3.5 text-slate-300">Amazon SDE-1</td>
          <td class="px-4 py-3.5">
            <span class="px-2.5 py-0.5 rounded text-xs font-semibold border ${stageColor}">
              ${currentStage}
            </span>
          </td>
          <td class="px-4 py-3.5">
            <button onclick="advanceCandidateStage('${s.name}')" class="px-3 py-1 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-lg text-xs transition-all shadow-sm">
              Advance ➔
            </button>
          </td>
        </tr>
      `;
    }).join("");

  } catch (err) {
    console.error("Pipeline load error:", err);
  }
}

function advanceCandidateStage(name) {
  alert(`✅ Candidate ${name} advanced to next interview evaluation stage! Candidate notified via campus email.`);
}

// 9. Recruiter Campus Drive Forensics
async function loadRecruiterDriveForensics() {
  const select = document.getElementById("recruiter-drive-select");
  const driveId = select ? select.value || 1 : 1;
  const container = document.getElementById("recruiter-forensics-display");
  if (!container) return;

  try {
    const res = await fetch(`/api/drives/${driveId}/forensics`);
    const forensics = await res.json();

    container.innerHTML = `
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 p-5 rounded-2xl bg-slate-950 border border-slate-800">
        <div>
          <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Drive Role & Package</span>
          <div class="text-xl font-extrabold text-white mt-1">${forensics.company_name} - ${forensics.role_title}</div>
          <div class="text-sm font-bold text-cyan-400 mt-0.5">${forensics.ctc_lpa} LPA (Super Dream Tier)</div>
        </div>
        <div>
          <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Campus Selection Rate</span>
          <div class="text-xl font-extrabold text-emerald-400 mt-1">${forensics.selection_rate}%</div>
          <div class="text-xs text-slate-400 mt-0.5">Based on historical campus performance</div>
        </div>
        <div>
          <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Priority Skill Filters</span>
          <p class="text-xs text-slate-300 mt-1">${forensics.frequent_topics}</p>
        </div>
      </div>

      <div class="space-y-3">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="git-commit" class="w-4 h-4 text-cyan-400"></i>
          Official Evaluation Rounds Structure
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          ${forensics.rounds.map(r => `
            <div class="p-4 bg-slate-900 border border-slate-800 rounded-2xl space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-extrabold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300">ROUND ${r.round}</span>
                <span class="text-xs text-slate-400 font-semibold">${r.duration}</span>
              </div>
              <div class="text-sm font-bold text-white">${r.name}</div>
              <p class="text-xs text-slate-300 leading-relaxed">${r.focus}</p>
            </div>
          `).join("")}
        </div>
      </div>

      <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs text-slate-300 space-y-1">
        <span class="font-bold text-amber-300 flex items-center gap-1.5">
          <i data-lucide="shield-alert" class="w-3.5 h-3.5 text-amber-400"></i>
          Recruiter Interviewer Guidelines:
        </span>
        <p class="italic text-slate-300">${forensics.interview_tips}</p>
      </div>
    `;

    if (window.lucide) lucide.createIcons();

  } catch (err) {
    console.error("Forensics error:", err);
  }
}

// 10. TPO Placement Analytics
async function loadTPOAnalytics() {
  try {
    const res = await fetch("/api/analytics/tpo-dashboard");
    const data = await res.json();
    const kpis = data.kpis;

    const kpiGrid = document.getElementById("tpo-kpi-grid");
    if (kpiGrid) {
      kpiGrid.innerHTML = `
        <div class="glass-card p-5 rounded-2xl space-y-1 border border-slate-800">
          <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Total Batch Size</span>
          <div class="text-2xl font-extrabold text-white">${kpis.total_students} Students</div>
          <div class="text-[11px] text-slate-500">2026 Graduating Class</div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-1 border border-slate-800">
          <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Placement Rate</span>
          <div class="text-2xl font-extrabold text-emerald-400">${kpis.placement_rate_pct}%</div>
          <div class="text-[11px] text-emerald-400/80">Active Season Metric</div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-1 border border-slate-800">
          <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Average Package</span>
          <div class="text-2xl font-extrabold text-cyan-400">${kpis.average_ctc_lpa} LPA</div>
          <div class="text-[11px] text-cyan-400/80">Campus Median CTC</div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-1 border border-rose-500/20 bg-rose-500/5">
          <span class="text-xs text-rose-300 uppercase font-bold tracking-wider">At-Risk Students</span>
          <div class="text-2xl font-extrabold text-rose-400">${kpis.at_risk_students_count}</div>
          <div class="text-[11px] text-rose-400/80">Early Intervention Active</div>
        </div>
      `;
    }

    // At-Risk Table
    const tbody = document.getElementById("tpo-at-risk-tbody");
    if (tbody) {
      tbody.innerHTML = data.at_risk_students.map(s => `
        <tr class="hover:bg-slate-900/60 transition-colors">
          <td class="px-4 py-3.5 font-bold text-white">${s.name}</td>
          <td class="px-4 py-3.5 text-slate-400 font-mono text-xs">${s.roll_no}</td>
          <td class="px-4 py-3.5 text-slate-300">${s.department}</td>
          <td class="px-4 py-3.5 font-bold text-rose-400">${s.cgpa}</td>
          <td class="px-4 py-3.5 text-rose-400 font-bold">${s.backlogs}</td>
          <td class="px-4 py-3.5"><span class="px-2.5 py-0.5 rounded text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">At-Risk</span></td>
          <td class="px-4 py-3.5">
            <button onclick="alert('Student ${s.name} successfully enrolled into ${s.suggested_cohort}!')" class="px-3 py-1 bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-xl text-xs font-bold transition-all shadow-sm">
              Assign to ${s.suggested_cohort}
            </button>
          </td>
        </tr>
      `).join("");
    }

    // Cohorts
    const cohortsGrid = document.getElementById("cohorts-grid");
    if (cohortsGrid) {
      cohortsGrid.innerHTML = data.active_cohorts.map(c => `
        <div class="p-5 glass-card rounded-2xl space-y-2.5">
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-white">${c.name}</span>
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-semibold border border-emerald-500/30">${c.category}</span>
          </div>
          <p class="text-xs text-slate-400">Mentor: <strong class="text-slate-200">${c.mentor}</strong></p>
          <p class="text-xs text-slate-300 bg-slate-950/70 p-2.5 rounded-xl border border-slate-800 font-mono">Weekly Focus: ${c.weekly_task}</p>
        </div>
      `).join("");
    }

    if (window.lucide) lucide.createIcons();

  } catch (err) {
    console.error("TPO load error:", err);
  }
}
