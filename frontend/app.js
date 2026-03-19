async function analyzeResume() {
  const analyzeBtn = document.getElementById("analyze-btn");
  const btnText = document.getElementById("btn-text");
  const spinner = document.getElementById("loading-spinner");
  const errorDiv = document.getElementById("match-error");

  errorDiv.textContent = "";

  const resumeFile = document.getElementById("resume").files[0];
  const jobTitle = document.getElementById("job_title").value.trim();
  const jdText = document.getElementById("jd").value.trim();

  // Basic client-side validation
  if (!resumeFile || !jobTitle || !jdText) {
    errorDiv.textContent = "Please fill in all fields and upload a PDF.";
    return;
  }
  
  // Show loading state
  btnText.textContent = "Analyzing...";
  spinner.classList.remove("hidden");
  analyzeBtn.disabled = true;

  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("job_title", jobTitle);
  formData.append("jd", jdText);

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) {
      errorDiv.textContent = data.detail || "Failed to analyze match.";
      return;
    }

    renderResults(data);
  } catch (err) {
    console.error(err);
    errorDiv.textContent = "Error connecting to server.";
  } finally {
    btnText.textContent = "Analyze Match";
    spinner.classList.add("hidden");
    analyzeBtn.disabled = false;
  }
}

function renderResults(data) {
  document.getElementById("empty-state").classList.add("hidden");
  document.getElementById("results-container").classList.remove("hidden");

  // Score
  const scoreEl = document.getElementById("match-score");
  const circleEl = document.getElementById("score-circle");
  scoreEl.textContent = `${data.score}%`;

  // Color code the score circle
  circleEl.classList.remove("high", "medium", "low");
  if (data.score >= 70) circleEl.classList.add("high");
  else if (data.score >= 40) circleEl.classList.add("medium");
  else circleEl.classList.add("low");

  // Skill counts
  document.getElementById("matched-count").textContent =
    data.matched_skills.length;
  document.getElementById("missing-count").textContent =
    data.missing_skills.length;

  // Render skill tags
  document.getElementById("overlap-skills").innerHTML = formatSkills(
    data.matched_skills,
  );
  document.getElementById("missing-skills").innerHTML = formatSkills(
    data.missing_skills,
  );
}

function formatSkills(skills) {
  if (!skills || skills.length === 0) return "<span>None</span>";
  return skills.map((s) => `<span>${s}</span>`).join("");
}
