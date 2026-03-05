import customtkinter as ctk
from tkinter import messagebox
import webbrowser

# ---------- THEME ----------
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class SkillNovaPro(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SkillNova Pro")
        self.geometry("1280x900")

        # Vibrant Colors
        self.navy_blue = "#1e3a8a"
        self.neon_blue = "#2563eb"
        self.purple = "#7c3aed"
        self.green = "#10b981"
        self.orange = "#f97316"
        self.card = "#f1f5f9"

        # State
        self.user_name = ctk.StringVar()
        self.user_skills = ctk.StringVar()
        self.selected_company = ctk.StringVar()
        self.capable_company = ctk.StringVar()
        self.readiness_score = 0

        # Company Skill Database
        self.company_requirements = {
            "Google": ["System Design", "Advanced DSA", "C++", "Cloud"],
            "Microsoft": ["C#", "Azure", "System Design", "Typescript"],
            "Deloitte": ["SQL", "Power BI", "Excel", "Analytics"],
            "TCS": ["Java", "DBMS", "Python", "Testing"],
            "Default": ["Programming", "DSA", "Database", "Networking"]
        }

        self.main = ctk.CTkFrame(self, fg_color="white")
        self.main.pack(fill="both", expand=True)

        self.render_landing()

    # ---------- UTIL ----------
    def clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ---------- LANDING ----------
    def render_landing(self):
        self.clear()

        ctk.CTkLabel(
            self.main,
            text="SKILLNOVA",
            font=("Arial", 70, "bold"),
            text_color=self.purple
        ).pack(pady=80)

        ctk.CTkButton(
            self.main,
            text="Start Journey",
            height=60,
            width=320,
            fg_color=self.neon_blue,
            command=self.render_login
        ).pack()

    # ---------- LOGIN ----------
    def render_login(self):
        self.clear()

        card = ctk.CTkFrame(self.main, fg_color=self.card, width=400, height=350)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Enter Name", font=("Arial", 26, "bold")).pack(pady=30)

        self.name_entry = ctk.CTkEntry(card, width=280)
        self.name_entry.pack(pady=20)

        ctk.CTkButton(
            card,
            text="Continue",
            fg_color=self.neon_blue,
            command=self.auth
        ).pack(pady=20)

    def auth(self):
        if self.name_entry.get():
            self.user_name.set(self.name_entry.get())
            self.render_skill_input()

    # ---------- SKILL INPUT ----------
    def render_skill_input(self):
        self.clear()

        ctk.CTkLabel(
            self.main,
            text="Enter Your Skills",
            font=("Arial", 32, "bold"),
            text_color=self.purple
        ).pack(pady=40)

        self.skill_entry = ctk.CTkEntry(
            self.main,
            width=500,
            height=50,
            placeholder_text="Python, SQL, DSA ..."
        )
        self.skill_entry.pack(pady=20)

        self.dream_entry = ctk.CTkEntry(
            self.main,
            width=500,
            height=50,
            placeholder_text="Dream Company (Optional)"
        )
        self.dream_entry.pack(pady=20)

        ctk.CTkButton(
            self.main,
            text="Analyze Profile",
            fg_color=self.orange,
            height=50,
            command=self.process_analysis
        ).pack(pady=20)

    # ---------- MATCH LOGIC ----------
    def find_best_company_match(self, skills):

        best_company = None
        best_score = -1

        for company, reqs in self.company_requirements.items():

            if company == "Default":
                continue

            score = sum(1 for r in reqs if r.lower() in skills)

            if score > best_score:
                best_score = score
                best_company = company

        if best_company is None:
            best_company = "TCS"

        return best_company, best_score

    def calculate_readiness(self, company, skills):
        required = self.company_requirements.get(company, self.company_requirements["Default"])
        match = sum(1 for r in required if r.lower() in skills)

        if len(required) == 0:
            return 0

        return match / len(required)

    # ---------- PROCESS ----------
    def process_analysis(self):
        skills = [s.strip().lower() for s in self.skill_entry.get().split(",")]

        best_company, _ = self.find_best_company_match(skills)
        self.capable_company.set(best_company)

        dream = self.dream_entry.get()
        if dream:
            self.selected_company.set(dream)
        else:
            self.selected_company.set(best_company)

        self.readiness_score = self.calculate_readiness(self.selected_company.get(), skills)

        self.render_result()

    # ---------- RESULT ----------
    def render_result(self):
        self.clear()

        ctk.CTkLabel(
            self.main,
            text=f"Welcome {self.user_name.get()}",
            font=("Arial", 30, "bold"),
            text_color=self.neon_blue
        ).pack(pady=20)

        # Capable Company Box
        cap = ctk.CTkFrame(self.main, fg_color="#dcfce7")
        cap.pack(padx=60, fill="x", pady=10)

        ctk.CTkLabel(
            cap,
            text=f"You Are Strongly Capable For: {self.capable_company.get()}",
            font=("Arial", 20, "bold"),
            text_color="#065f46"
        ).pack(pady=15)

        # Target Company Box
        tar = ctk.CTkFrame(self.main, fg_color="#e0e7ff")
        tar.pack(padx=60, fill="x", pady=10)

        ctk.CTkLabel(
            tar,
            text=f"Your Target Company: {self.selected_company.get()}",
            font=("Arial", 20, "bold"),
            text_color=self.navy_blue
        ).pack(pady=15)

        self.render_gap_report()

    # ---------- GAP REPORT ----------
    def render_gap_report(self):

        needed = self.company_requirements.get(
            self.selected_company.get(),
            self.company_requirements["Default"]
        )

        score_box = ctk.CTkFrame(self.main, fg_color=self.card)
        score_box.pack(pady=20, padx=60, fill="x")

        ctk.CTkLabel(
            score_box,
            text=f"Readiness Score: {int(self.readiness_score*100)}%",
            font=("Arial", 18, "bold"),
            text_color=self.purple
        ).pack(pady=10)

        progress = ctk.CTkProgressBar(score_box, width=500)
        progress.pack(pady=10)
        progress.set(self.readiness_score)

        ctk.CTkLabel(
            self.main,
            text="Required Skills Roadmap",
            font=("Arial", 22, "bold"),
            text_color=self.neon_blue
        ).pack(pady=20)

        skill_frame = ctk.CTkFrame(self.main, fg_color="white")
        skill_frame.pack(padx=80, fill="x")

        for skill in needed:
            row = ctk.CTkFrame(skill_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(
                row,
                text=f"• {skill}",
                font=("Arial", 16)
            ).pack(side="left", padx=20)

            link = f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+roadmap"

            ctk.CTkButton(
                row,
                text="Learn",
                width=100,
                fg_color=self.orange,
                command=lambda l=link: webbrowser.open(l)
            ).pack(side="right", padx=20)


# ---------- RUN ----------
if __name__ == "__main__":
    app = SkillNovaPro()
    app.mainloop()
