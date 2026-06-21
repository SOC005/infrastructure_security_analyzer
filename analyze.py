import pandas as pd

print("=" * 60)
print("   Infrastructure Security Analyzer")
print("   Powered by DevSecOps Pipeline")
print("=" * 60)

df = pd.read_excel("dataset.xlsx")
total = len(df)
print(f"\nTotal records analyzed: {total}\n")

# 1. Vulnerability Severity
print("── 1. Vulnerability Severity Breakdown ──")
severity = df["Vulnerability_Severity"].value_counts()
for level, count in severity.items():
    print(f"   {level:<10} : {count} issues")

# 2. Critical + High
print("\n── 2. Critical & High Risk Dependencies ──")
risky = df[df["Vulnerability_Severity"].isin(["Critical", "High"])]
print(f"   Total Critical/High vulnerabilities: {len(risky)}")
print(risky[["Infrastructure_File", "Application_Dependency",
             "Dependency_Version", "Vulnerability_Severity"]].to_string(index=False))

# 3. Publicly Accessible Resources
print("\n── 3. Publicly Accessible Resources ──")
exposed = df[df["Public_Access"] == "Yes"]
print(f"   Total publicly exposed resources: {len(exposed)}")
print(exposed[["Infrastructure_File", "Resource_Type",
               "Port_Configuration", "Vulnerability_Severity"]].to_string(index=False))

# 4. Dangerous Open Ports
print("\n── 4. Dangerous Open Ports ──")
dangerous_ports = [21, 22, 23, 25, 3306, 6379]
danger_df = df[df["Port_Configuration"].isin(dangerous_ports)]
print(f"   Resources with dangerous ports open: {len(danger_df)}")
print(df["Port_Configuration"].value_counts().to_string())

# 5. CI/CD Pipeline Status
print("\n── 5. CI/CD Pipeline Status ──")
status = df["CI_CD_Pipeline_Status"].value_counts()
for s, count in status.items():
    print(f"   {s:<10} : {count}")

# 6. Most Vulnerable Dependencies
print("\n── 6. Most Vulnerable Dependencies ──")
dep = df[df["Vulnerability_Severity"].isin(["Critical", "High"])]\
    .groupby("Application_Dependency").size()\
    .sort_values(ascending=False).head(8)
print(dep.to_string())

# 7. Resource Type Breakdown
print("\n── 7. Resource Type Breakdown ──")
print(df["Resource_Type"].value_counts().to_string())

# 8. HIGHEST RISK: Public + Critical/High
print("\n── 8. HIGHEST RISK: Public + Critical/High Vulnerabilities ──")
top_danger = df[
    (df["Public_Access"] == "Yes") &
    (df["Vulnerability_Severity"].isin(["Critical", "High"]))
]
print(f"   Total top-risk entries: {len(top_danger)}")
print(top_danger[["Infrastructure_File", "Resource_Type",
                   "Application_Dependency", "Vulnerability_Severity",
                   "Port_Configuration"]].to_string(index=False))

# 9. Failed Pipelines with Critical Issues
print("\n── 9. Failed Pipelines with Critical Issues ──")
failed_critical = df[
    (df["CI_CD_Pipeline_Status"] == "Failed") &
    (df["Vulnerability_Severity"].isin(["Critical", "High"]))
]
print(f"   Total failed + critical/high: {len(failed_critical)}")

print("\n" + "=" * 60)
print("   Security Analysis Complete")
print("=" * 60)
