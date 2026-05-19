import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import io

st.set_page_config(
    page_title="DGDM Rule Tracker",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #F7F6F2;
}

section[data-testid="stSidebar"] {
    background-color: #1A1A2E;
}

section[data-testid="stSidebar"] * {
    color: #E8E6E0 !important;
}

section[data-testid="stSidebar"] h2 {
    color: #E8E6E0 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 1.5rem !important;
}

section[data-testid="stSidebar"] label {
    color: #9A97B0 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stSelectbox > div > div > div {
    background-color: #2C2C4A !important;
    border: 1px solid #3D3D6B !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .stSelectbox span,
section[data-testid="stSidebar"] .stSelectbox p,
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] .stDateInput > div > div > input {
    background-color: #2C2C4A !important;
    border: 1px solid #3D3D6B !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .stDateInput > div > div {
    background-color: #2C2C4A !important;
    border: 1px solid #3D3D6B !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] svg {
    fill: #9A97B0 !important;
    stroke: #9A97B0 !important;
}

section[data-testid="stSidebar"] button {
    background-color: #2C2C4A !important;
    border: 1px solid #3D3D6B !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] button:hover {
    background-color: #3D3D6B !important;
    border-color: #5A5A9A !important;
}

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px 22px;
    border: 1px solid #E8E6E0;
}

.metric-num {
    font-size: 32px;
    font-weight: 600;
    line-height: 1;
    margin-bottom: 4px;
}

.metric-lbl {
    font-size: 12px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.day-section {
    background: white;
    border-radius: 14px;
    border: 1px solid #E8E6E0;
    margin-bottom: 16px;
    overflow: hidden;
}

.day-header {
    padding: 14px 20px;
    border-bottom: 1px solid #F0EEE8;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.day-name {
    font-size: 15px;
    font-weight: 600;
    color: #1A1A2E;
}

.day-pills {
    display: flex;
    gap: 6px;
    align-items: center;
}

.pill {
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 500;
}

.pill-critical { background: #FEE8E8; color: #B91C1C; }
.pill-high     { background: #FEF3CD; color: #92400E; }
.pill-medium   { background: #E0F0FF; color: #1D4ED8; }
.pill-done     { background: #D1FAE5; color: #065F46; }

.rule-item {
    padding: 12px 20px;
    border-bottom: 1px solid #F7F6F2;
    display: flex;
    align-items: flex-start;
    gap: 14px;
}

.rule-item:last-child { border-bottom: none; }

.prio-bar {
    width: 3px;
    border-radius: 2px;
    flex-shrink: 0;
    align-self: stretch;
    min-height: 40px;
}

.bar-critical { background: #DC2626; }
.bar-high     { background: #D97706; }
.bar-medium   { background: #2563EB; }

.rule-content { flex: 1; min-width: 0; }

.rule-name {
    font-size: 13px;
    font-weight: 500;
    color: #1A1A2E;
    margin-bottom: 3px;
}

.rule-why {
    font-size: 12px;
    color: #666;
    line-height: 1.5;
    margin-bottom: 6px;
}

.tag-row { display: flex; gap: 5px; flex-wrap: wrap; }

.tag {
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 20px;
    font-weight: 500;
}

.tag-safety { background: #FEE2E2; color: #991B1B; }
.tag-reg    { background: #FEF9C3; color: #713F12; }
.tag-data   { background: #DBEAFE; color: #1E40AF; }

.done-rule { opacity: 0.45; }

.export-btn-wrap {
    display: flex;
    gap: 10px;
    margin-top: 8px;
}

.progress-outer {
    background: #F0EEE8;
    border-radius: 4px;
    height: 6px;
    width: 100%;
    margin-top: 8px;
}

.stCheckbox label {
    font-size: 13px !important;
    color: #1A1A2E !important;
}

div[data-testid="stMarkdownContainer"] p {
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

RULES = [
    {
        "id": "R01",
        "day": "Monday",
        "name": "Rx flag for Schedule H, H1, X, NDPS drugs",
        "why": "Schedule H/H1/X/NDPS drugs must be Rx=1. Selling OTC violates the Drugs & Cosmetics Act — direct patient safety risk.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 5,
        "owner": "Mukesh",
        "sheet": "Defined_SH_then_Rx_yes"
    },
    {
        "id": "R02",
        "day": "Monday",
        "name": "Cold chain products → Rx=1",
        "why": "Insulin, vaccines, biologics sold without Rx can cause serious patient harm. Non-negotiable compliance.",
        "tags": ["Patient safety"],
        "priority": "Critical",
        "est_min": 3,
        "owner": "Mukesh",
        "sheet": "Coldchain_yes_Then_Rx_Yes"
    },
    {
        "id": "R03",
        "day": "Monday",
        "name": "Habit forming = 1 → Rx must be 1",
        "why": "Habit-forming drugs (opioids, benzodiazepines) without Rx flag expose platform to narcotics law violations.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 3,
        "owner": "Mukesh",
        "sheet": "habit_forming_1_rx_1"
    },
    {
        "id": "R04",
        "day": "Monday",
        "name": "Rx=1 → OTC must be 0",
        "why": "Rx=1 and OTC=1 simultaneously creates contradictory dispensing logic — product may be sold without prescription when it should not be.",
        "tags": ["Patient safety"],
        "priority": "Critical",
        "est_min": 3,
        "owner": "Mukesh",
        "sheet": "Rx_1_then_otc_0"
    },
    {
        "id": "R05",
        "day": "Monday",
        "name": "Composition classification 'Antibiotic' → Rx=1",
        "why": "OTC antibiotics are banned in India. Incorrect Rx flag directly contributes to antibiotic resistance and regulatory violation.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 4,
        "owner": "Mukesh",
        "sheet": "CompClass_Antib_Then_Rx_yes"
    },
    {
        "id": "R06",
        "day": "Monday",
        "name": "Antibiotic composition → Schedule H or H1 only",
        "why": "All antibiotics in India must be Schedule H or H1 per CDSCO guidelines. Any other schedule is a cataloguing error with legal consequence.",
        "tags": ["Regulatory"],
        "priority": "High",
        "est_min": 4,
        "owner": "Mukesh",
        "sheet": "Compclass_antib_then_SH_H_or_H1"
    },
    {
        "id": "R07",
        "day": "Monday",
        "name": "All parenterals (injectables, infusions, vaccines) → Rx=1",
        "why": "Injectables/vaccines are prescription-only under Indian pharma law. Wrong Rx flag = unlawful OTC sale.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 4,
        "owner": "Mukesh",
        "sheet": "PrdtForm_Injectibles_then_defined_SH"
    },
    {
        "id": "R08",
        "day": "Monday",
        "name": "FMCG / Surgical business head → Rx must be 0",
        "why": "FMCG products should never have Rx=1. False Rx flag restricts genuine OTC products and confuses customers.",
        "tags": ["Data integrity"],
        "priority": "Medium",
        "est_min": 4,
        "owner": "Mukesh",
        "sheet": "BH_FMCG_or_SX_Then_Rx_No"
    },
    {
        "id": "R09",
        "day": "Tuesday",
        "name": "Cough syrups (BH: medicines, Sub-cat: cough & cold) → Rx=1",
        "why": "CDSCO made codeine-based cough syrups prescription-only. Incorrect Rx flag enables misuse/abuse.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 5,
        "owner": "Dipika",
        "sheet": "cough_syp_bh_medicine_rx_1"
    },
    {
        "id": "R10",
        "day": "Tuesday",
        "name": "FMCG / AYUSH business head → Schedule = Non-Schedule",
        "why": "AYUSH and FMCG products with Schedule H/H1/X tag is a serious error — triggers unnecessary dispensing controls on OTC products.",
        "tags": ["Regulatory"],
        "priority": "High",
        "est_min": 4,
        "owner": "Mukesh/Sneha",
        "sheet": "BH_FMCG_or_SX_Then_SH_NonSH"
    },
    {
        "id": "R11",
        "day": "Tuesday",
        "name": "Drug with composition/ingredient → Schedule field not blank",
        "why": "Blank schedule on any drug with a composition makes dispensing rules unknown. Pharmacist cannot safely process the order.",
        "tags": ["Patient safety"],
        "priority": "Critical",
        "est_min": 5,
        "owner": "Mukesh/Sneha",
        "sheet": "Comp_or_Ing_Then_SH_not_blank"
    },
    {
        "id": "R12",
        "day": "Tuesday",
        "name": "Speciality flag = 1 → Rx=1, OTC=0",
        "why": "Specialty drugs (oncology, biologics) are high-risk. Without Rx=1 they can be dispensed without supervision — serious patient harm risk.",
        "tags": ["Patient safety"],
        "priority": "Critical",
        "est_min": 6,
        "owner": "Mukesh",
        "sheet": "speciality-1-rx-1-otc-0"
    },
    {
        "id": "R13",
        "day": "Wednesday",
        "name": "DPCO products — selling price must be ≤ price cap (PCP)",
        "why": "DPCO is enforced by NPPA. Selling above MRP/PCP is a cognizable offence. Protects platform from legal action.",
        "tags": ["Regulatory"],
        "priority": "High",
        "est_min": 7,
        "owner": "Dipika",
        "sheet": "dpco_pcp_selling_rate_validation"
    },
    {
        "id": "R14",
        "day": "Wednesday",
        "name": "Same composition + Available-in → all banned drugs must be banned",
        "why": "If a molecule combination is banned by CDSCO, ALL its variants must be banned. Partial banning leaves dangerous drugs live.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 7,
        "owner": "Dipika",
        "sheet": "SameComp_SameAvail_then_alldrugs_ban"
    },
    {
        "id": "R15",
        "day": "Wednesday",
        "name": "Same group ID → same GST, Rx, Business Category, Cold-chain",
        "why": "Inconsistent attributes within a group ID cause wrong tax filing, incorrect dispensing logic, and cold chain mishandling.",
        "tags": ["Data integrity", "Regulatory"],
        "priority": "High",
        "est_min": 6,
        "owner": "Mukesh",
        "sheet": "Same_groupID_then_same_attributes"
    },
    {
        "id": "R16",
        "day": "Every 10 Days",
        "name": "Schedule H1 molecule list → H1 tagging in composition master",
        "why": "H1 molecules have stricter dispensing rules. Missing H1 tag in composition master flows wrong schedule to all drugs using that molecule.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "High",
        "est_min": 8,
        "owner": "Mukesh",
        "sheet": "Schedule H1_Molecule"
    },
    {
        "id": "R17",
        "day": "Every 10 Days",
        "name": "Habit forming molecule list → habit forming flag = yes in composition master",
        "why": "If a habit-forming molecule is not flagged, all derived drugs lose their habit-forming tag → Rx=0 drugs dispensed without prescription.",
        "tags": ["Patient safety"],
        "priority": "High",
        "est_min": 8,
        "owner": "Mukesh",
        "sheet": "Habit Forming_Molecule"
    },
    {
        "id": "R18",
        "day": "Every 10 Days",
        "name": "Liquid formulations → composition must have 'per ml' tag",
        "why": "Liquid drug dosing is per ml. Without the per ml tag, dosage calculations (especially paediatric) are impossible — critical safety.",
        "tags": ["Patient safety"],
        "priority": "High",
        "est_min": 7,
        "owner": "Mukesh",
        "sheet": "available_in_syrup_suspension_composition_per_ml"
    },
    {
        "id": "R19",
        "day": "Every 10 Days",
        "name": "Same molecule combination → same schedule across all strengths",
        "why": "Identical molecules with different strengths cannot have different schedules. Inconsistency confuses pharmacists and violates dispensing norms.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "High",
        "est_min": 7,
        "owner": "Mukesh/Sneha",
        "sheet": "Mol_comb_same_str_then_same_SH"
    },
    {
        "id": "R20",
        "day": "Every 10 Days",
        "name": "Pack UOM from defined list only (Tablet, ml, gm, Capsule etc.)",
        "why": "Free-text UOM values break dosage logic, e-prescription parsing, and customer-facing dose instructions.",
        "tags": ["Data integrity"],
        "priority": "Medium",
        "est_min": 5,
        "owner": "Dipika",
        "sheet": "UOM_Update_Define_List"
    },
    {
        "id": "R21",
        "day": "Thursday",
        "name": "Schedule–habit forming–composition classification combination validation",
        "why": "An incorrect schedule+habit forming+composition class combination (e.g. non-schedule on a known narcotic) bypasses pharmacist controls and exposes patients to dangerous drugs without supervision.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 8,
        "owner": "Mukesh/Sneha",
        "sheet": "schedule-comp-class-habit-forming"
    },
    {
        "id": "R22",
        "day": "Thursday",
        "name": "Same Rx value across same molecule combination (all strengths, excl. injectables)",
        "why": "Same molecule in different strengths must have the same Rx value. Inconsistency means one variant is dispensed OTC while another requires prescription — patient safety gap.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 7,
        "owner": "Mukesh",
        "sheet": "prescription-required-online_comp."
    },
    {
        "id": "R23",
        "day": "Thursday",
        "name": "Composition with (NA) strength & UOM → Rx=1",
        "why": "Compositions with NA strength/UOM are often undocumented potent molecules. Defaulting Rx=0 on these allows unregulated sale of potentially dangerous formulations.",
        "tags": ["Patient safety"],
        "priority": "Critical",
        "est_min": 5,
        "owner": "Mukesh",
        "sheet": "prescription-required-online_comp(na)"
    },
    {
        "id": "R24",
        "day": "Thursday",
        "name": "AYUSH business head → Schedule Non-Schedule, E, or E1 only",
        "why": "AYUSH products are regulated separately from allopathic drugs. Assigning Schedule H/H1/X to AYUSH items creates false dispensing restrictions and confuses the pharmacist workflow.",
        "tags": ["Regulatory"],
        "priority": "High",
        "est_min": 4,
        "owner": "Mukesh/Sneha",
        "sheet": "BH_AYUSH_Then_SH_NonSH_and_E1_and_E"
    },
    {
        "id": "R25",
        "day": "Friday",
        "name": "Composition classification 'Antibiotic' → Schedule H or H1 cross-check with Rx=1",
        "why": "Weekly cross-check catch-all: antibiotics that slipped through Mon/Thu checks. Any antibiotic without both Schedule H/H1 AND Rx=1 is a live compliance breach before the weekend.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 7,
        "owner": "Mukesh",
        "sheet": "CompClass_Antib_Then_Rx_yes"
    },
    {
        "id": "R26",
        "day": "Friday",
        "name": "All parenterals → Schedule H, H1, G, G+H, or Non-Schedule (caution advised)",
        "why": "Injectables/infusions/vaccines must fall in a valid schedule. A blank or wrong schedule on a parenteral before weekend means no pharmacist can legally dispense it correctly.",
        "tags": ["Patient safety", "Regulatory"],
        "priority": "Critical",
        "est_min": 6,
        "owner": "Mukesh/Sneha",
        "sheet": "PrdtForm_Injectibles_then_defined_SH"
    },
    {
        "id": "R27",
        "day": "Friday",
        "name": "Molecule-only composition → composition-classification must be single & consistent",
        "why": "A molecule used alone or in combination cannot have multiple composition classifications in the master table. Inconsistency cascades to hundreds of SKUs with wrong Rx, schedule, and habit-forming flags.",
        "tags": ["Patient safety", "Data integrity"],
        "priority": "Critical",
        "est_min": 8,
        "owner": "Mukesh",
        "sheet": "composition-classification_Molecule"
    },
    {
        "id": "R28",
        "day": "Friday",
        "name": "Prescription by field → valid values when Rx=1 (Customer, BAMS, MBBS)",
        "why": "If Rx=1 but 'Prescription by' is blank or has an invalid value, the platform cannot enforce who can write the prescription — a direct regulatory and liability gap.",
        "tags": ["Regulatory"],
        "priority": "High",
        "est_min": 5,
        "owner": "Shraddha",
        "sheet": "Rx-(Rx=1, prescription by= Customer, BAMS, MBBS)"
    }
]

DATA_FILE = "tracker_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_date_key(d):
    return d.strftime("%Y-%m-%d")

def get_rule_key(rule_id, date_key):
    return f"{date_key}_{rule_id}"

data = load_data()

ALL_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Every 10 Days"]

with st.sidebar:
    st.markdown("## 🧬 DGDM Tracker")
    st.markdown("---")

    st.markdown("## Filters")
    selected_day = st.selectbox(
        "Day / Frequency",
        ["All"] + ALL_DAYS,
        index=0
    )

    selected_priority = st.selectbox(
        "Priority",
        ["All", "Critical", "High", "Medium"],
        index=0
    )

    selected_date = st.date_input(
        "Tracking date",
        value=date.today()
    )

    date_key = get_date_key(selected_date)

    st.markdown("---")
    st.markdown("## Export")

    if st.button("📥 Export today's report", use_container_width=True):
        export_rows = []
        for rule in RULES:
            rk = get_rule_key(rule["id"], date_key)
            done = data.get(rk, {}).get("done", False)
            done_at = data.get(rk, {}).get("done_at", "")
            notes = data.get(rk, {}).get("notes", "")
            export_rows.append({
                "Rule ID": rule["id"],
                "Day": rule["day"],
                "Rule Name": rule["name"],
                "Priority": rule["priority"],
                "Owner": rule["owner"],
                "Sheet": rule["sheet"],
                "Est. Time (min)": rule["est_min"],
                "Done": "Yes" if done else "No",
                "Completed At": done_at,
                "Notes": notes,
                "Tracking Date": date_key
            })
        df_export = pd.DataFrame(export_rows)
        csv_buf = io.StringIO()
        df_export.to_csv(csv_buf, index=False)
        st.download_button(
            label="⬇ Download CSV",
            data=csv_buf.getvalue(),
            file_name=f"dgdm_tasks_{date_key}.csv",
            mime="text/csv",
            use_container_width=True
        )

    if st.button("📥 Export full history", use_container_width=True):
        all_rows = []
        all_dates = set()
        for key in data.keys():
            parts = key.rsplit("_", 1)
            if len(parts) == 2:
                all_dates.add(parts[0])
        for d_key in sorted(all_dates):
            for rule in RULES:
                rk = get_rule_key(rule["id"], d_key)
                done = data.get(rk, {}).get("done", False)
                done_at = data.get(rk, {}).get("done_at", "")
                notes = data.get(rk, {}).get("notes", "")
                all_rows.append({
                    "Tracking Date": d_key,
                    "Rule ID": rule["id"],
                    "Day": rule["day"],
                    "Rule Name": rule["name"],
                    "Priority": rule["priority"],
                    "Owner": rule["owner"],
                    "Done": "Yes" if done else "No",
                    "Completed At": done_at,
                    "Notes": notes
                })
        if all_rows:
            df_all = pd.DataFrame(all_rows)
            csv_all = io.StringIO()
            df_all.to_csv(csv_all, index=False)
            st.download_button(
                label="⬇ Download full history CSV",
                data=csv_all.getvalue(),
                file_name=f"dgdm_history_all.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No history found yet.")

    st.markdown("---")
    if st.button("🔄 Reset today's tasks", use_container_width=True):
        for rule in RULES:
            rk = get_rule_key(rule["id"], date_key)
            if rk in data:
                del data[rk]
        save_data(data)
        st.rerun()

filtered_rules = [
    r for r in RULES
    if (selected_day == "All" or r["day"] == selected_day)
    and (selected_priority == "All" or r["priority"] == selected_priority)
]

total = len(filtered_rules)
done_count = sum(
    1 for r in filtered_rules
    if data.get(get_rule_key(r["id"], date_key), {}).get("done", False)
)
pct = int((done_count / total * 100)) if total > 0 else 0
total_min = sum(r["est_min"] for r in filtered_rules)
done_min = sum(
    r["est_min"] for r in filtered_rules
    if data.get(get_rule_key(r["id"], date_key), {}).get("done", False)
)
remaining_min = total_min - done_min

st.markdown(f"""
<div style='display:flex;align-items:baseline;gap:10px;margin-bottom:4px'>
  <span style='font-size:26px;font-weight:700;color:#1A1A2E;font-family:"DM Sans",sans-serif'>DGDM Rule Tracker</span>
  <span style='font-size:13px;color:#888;font-family:"DM Mono",monospace'>{selected_date.strftime("%A, %d %b %Y")}</span>
</div>
<div style='font-size:13px;color:#666;margin-bottom:20px'>Priority pharma data quality checks · Patient safety first</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card">
    <div class="metric-num" style="color:#1A1A2E">{done_count}<span style="font-size:18px;color:#bbb">/{total}</span></div>
    <div class="metric-lbl">Rules completed</div>
    <div class="progress-outer"><div style="height:6px;border-radius:4px;background:{'#059669' if pct==100 else '#2563EB'};width:{pct}%"></div></div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-card">
    <div class="metric-num" style="color:#059669">{pct}%</div>
    <div class="metric-lbl">Completion rate</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="metric-card">
    <div class="metric-num" style="color:#D97706">{remaining_min}</div>
    <div class="metric-lbl">Minutes remaining</div>
    </div>""", unsafe_allow_html=True)
with c4:
    critical_left = sum(
        1 for r in filtered_rules
        if r["priority"] == "Critical"
        and not data.get(get_rule_key(r["id"], date_key), {}).get("done", False)
    )
    st.markdown(f"""<div class="metric-card">
    <div class="metric-num" style="color:#DC2626">{critical_left}</div>
    <div class="metric-lbl">Critical rules pending</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

PRIO_COLOR = {"Critical": "#DC2626", "High": "#D97706", "Medium": "#2563EB"}
PRIO_BG    = {"Critical": "#FEE8E8", "High": "#FEF3CD", "Medium": "#E0F0FF"}
PRIO_TEXT  = {"Critical": "#B91C1C", "High": "#92400E", "Medium": "#1D4ED8"}
TAG_CLASS  = {"Patient safety": ("tag-safety", "🔴"), "Regulatory": ("tag-reg", "🟡"), "Data integrity": ("tag-data", "🔵")}

days_in_view = [d for d in ALL_DAYS if selected_day == "All" or d == selected_day]

for day in days_in_view:
    day_rules = [r for r in filtered_rules if r["day"] == day]
    if not day_rules:
        continue

    done_in_day = sum(
        1 for r in day_rules
        if data.get(get_rule_key(r["id"], date_key), {}).get("done", False)
    )
    critical_in_day = sum(1 for r in day_rules if r["priority"] == "Critical")
    high_in_day = sum(1 for r in day_rules if r["priority"] == "High")

    with st.container():
        st.markdown(f"""
        <div class="day-section">
          <div class="day-header">
            <div class="day-name">{day}</div>
            <div class="day-pills">
              <span class="pill pill-critical">{critical_in_day} critical</span>
              <span class="pill pill-high">{high_in_day} high</span>
              <span class="pill pill-done">{done_in_day}/{len(day_rules)} done</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    for rule in day_rules:
        rk = get_rule_key(rule["id"], date_key)
        is_done = data.get(rk, {}).get("done", False)
        saved_notes = data.get(rk, {}).get("notes", "")

        pcolor = PRIO_COLOR[rule["priority"]]
        pbg    = PRIO_BG[rule["priority"]]
        ptxt   = PRIO_TEXT[rule["priority"]]

        tag_html = " ".join([
            f'<span style="font-size:10px;padding:2px 8px;border-radius:20px;font-weight:500;background:{"#FEE2E2" if t=="Patient safety" else "#FEF9C3" if t=="Regulatory" else "#DBEAFE"};color:{"#991B1B" if t=="Patient safety" else "#713F12" if t=="Regulatory" else "#1E40AF"}">{t}</span>'
            for t in rule["tags"]
        ])

        done_style = "opacity:0.45;" if is_done else ""
        done_line  = "text-decoration:line-through;color:#aaa;" if is_done else ""

        st.markdown(f"""
        <div style="background:white;border-radius:10px;border:1px solid #E8E6E0;margin-bottom:8px;padding:14px 16px;{done_style}">
          <div style="display:flex;align-items:flex-start;gap:12px">
            <div style="width:3px;border-radius:2px;background:{pcolor};align-self:stretch;min-height:40px;flex-shrink:0"></div>
            <div style="flex:1;min-width:0">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
                <span style="font-size:10px;font-family:'DM Mono',monospace;color:#bbb">{rule['id']}</span>
                <span style="font-size:11px;padding:2px 8px;border-radius:20px;background:{pbg};color:{ptxt};font-weight:500">{rule['priority']}</span>
                <span style="font-size:11px;color:#aaa">~{rule['est_min']} min · {rule['owner']}</span>
              </div>
              <div style="font-size:13px;font-weight:500;color:#1A1A2E;margin-bottom:4px;{done_line}">{rule['name']}</div>
              <div style="font-size:12px;color:#666;line-height:1.55;margin-bottom:8px">{rule['why']}</div>
              <div style="margin-bottom:6px">{tag_html}</div>
              <div style="font-size:10px;font-family:'DM Mono',monospace;color:#bbb">sheet: {rule['sheet']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_check, col_notes = st.columns([1, 3])
        with col_check:
            checked = st.checkbox(
                f"Mark done",
                value=is_done,
                key=f"chk_{rk}"
            )
            if checked != is_done:
                if rk not in data:
                    data[rk] = {}
                data[rk]["done"] = checked
                data[rk]["done_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if checked else ""
                save_data(data)
                st.rerun()

        with col_notes:
            notes_input = st.text_input(
                "Notes / inconsistencies found",
                value=saved_notes,
                key=f"notes_{rk}",
                placeholder="e.g. Found 12 SKUs with incorrect Rx flag..."
            )
            if notes_input != saved_notes:
                if rk not in data:
                    data[rk] = {}
                data[rk]["notes"] = notes_input
                save_data(data)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

if done_count == total and total > 0:
    st.success(f"All {total} rules completed for {selected_date.strftime('%d %b %Y')}! Great work.")
