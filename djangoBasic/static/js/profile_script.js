document.addEventListener("DOMContentLoaded", function() {
    const maxItems = 3; // Maksymalna ilość elementów przed zastosowaniem kropek
  
    const cards = document.querySelectorAll(".user-card");
  
    cards.forEach(card => {
      const skillContainer = card.querySelector(".skill-container");
      const experienceContainer = card.querySelector(".experience-container");
      const bottomSection = card.querySelector(".bottom");
  
      const skillPills = skillContainer.querySelectorAll(".pill.skill");
      const experiencePills = experienceContainer.querySelectorAll(".pill.experience");
  
      if (skillPills.length > maxItems) {
        for (let i = maxItems; i < skillPills.length; i++) {
          skillPills[i].style.display = "none";
        }
        const dots = document.createElement("div");
        dots.classList.add("pill");
        dots.classList.add("skill");
        dots.textContent = "...";
        skillContainer.appendChild(dots);
      }
  
      if (experiencePills.length > maxItems) {
        for (let i = maxItems; i < experiencePills.length; i++) {
          experiencePills[i].style.display = "none";
        }
        const dots = document.createElement("div");
        dots.classList.add("pill");
        dots.classList.add("experience");
        dots.textContent = "...";
        experienceContainer.appendChild(dots);
      }
  
      // Check if bottom section is cut off
      const isBottomSectionCutOff = bottomSection.offsetTop + bottomSection.offsetHeight > card.offsetHeight;
      if (isBottomSectionCutOff) {
        const lastSkillPill = skillContainer.querySelector(".pill.skill:last-child");
        const lastExperiencePill = experienceContainer.querySelector(".pill.experience:last-child");
  
        if (lastSkillPill) {
          lastSkillPill.style.display = "none";
          skillContainer.querySelector(".pill.skill:nth-last-child(3)").style.display = "none";
          skillContainer.querySelector(".pill.skill:nth-last-child(2)").style.display = "none";
  
          const dots = document.createElement("div");
          dots.classList.add("pill");
          dots.classList.add("skill");
          dots.textContent = "...";
          skillContainer.appendChild(dots);
        }
  
        if (lastExperiencePill) {
          lastExperiencePill.style.display = "none";
          experienceContainer.querySelector(".pill.experience:nth-last-child(3)").style.display = "none";
          experienceContainer.querySelector(".pill.experience:nth-last-child(2)").style.display = "none";
  
          const dots = document.createElement("div");
          dots.classList.add("pill");
          dots.classList.add("experience");
          dots.textContent = "...";
          experienceContainer.appendChild(dots);
        }
      }
    });
  });
  