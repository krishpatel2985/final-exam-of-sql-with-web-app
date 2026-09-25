import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from database import (
    init_db,
    get_connection,
    run_query,
    get_kpis,
    get_table_names,
    get_table_data,
    get_table_schema,
    add_event,
    add_attendee,
    book_ticket,
    record_payment,
    update_ticket_price,
    delete_event
)
from queries import PROJECT_QUERIES

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Event Management System • SQL Portal",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS & DESIGN SYSTEM
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Background & Main Container */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 95%;
    }

    /* App Header Banner */
    .app-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(14, 165, 233, 0.12) 50%, rgba(139, 92, 246, 0.18) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .app-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #A5B4FC 0%, #38BDF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        letter-spacing: -0.02em;
    }
    .app-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.5;
    }

    /* KPI Bar */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 14px;
        margin-bottom: 26px;
    }
    .kpi-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 18px;
        backdrop-filter: blur(8px);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.45);
        box-shadow: 0 8px 20px -6px rgba(99, 102, 241, 0.25);
    }
    .kpi-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-top: 4px;
        line-height: 1.2;
    }
    .kpi-tag {
        font-size: 0.75rem;
        color: #38BDF8;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Content Cards */
    .card-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        backdrop-filter: blur(6px);
    }

    /* Pill Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.2);
        color: #C7D2FE;
        border: 1px solid rgba(99, 102, 241, 0.35);
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-teal {
        background: rgba(20, 184, 166, 0.2);
        color: #99F6E4;
        border-color: rgba(20, 184, 166, 0.35);
    }
    .badge-amber {
        background: rgba(245, 158, 11, 0.2);
        color: #FDE68A;
        border-color: rgba(245, 158, 11, 0.35);
    }

    /* Metric pill */
    .metric-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(15, 23, 42, 0.7);
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #E2E8F0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-right: 8px;
    }

    /* Sidebar Tweaks */
    section[data-testid="stSidebar"] {
        background-color: #0B0F19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------
init_db(force_reset=False)

# ---------------------------------------------------------
# HEADER BANNER
# ---------------------------------------------------------
st.markdown("""
<div class="app-header">
    <div class="app-title">🎭 Event Management System</div>
    <div class="app-subtitle">Interactive SQL Analytics & Management Web Application • Powered by Streamlit & Relational Database</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3898/3898082.png", width=65)
    st.title("Navigation")
    
    menu = st.radio(
        "Select Portal Module:",
        [
            "📊 Executive Dashboard",
            "🗄️ Database Explorer",
            "📈 Visual Analytics",
            "💡 SQL Queries Showcase",
            "⚡ Interactive SQL Console",
            "➕ Data Management (CRUD)",
            "🏗️ Relational Schema & ER"
        ],
        index=0
    )
    
    st.markdown("---")
    st.subheader("⚙️ System Control")
    if st.button("🔄 Reset Database to Default", use_container_width=True):
        init_db(force_reset=True)
        st.toast("Database reset to original exam state!", icon="✅")
        st.rerun()

    st.markdown("---")
    st.caption("📌 **Project**: Event Management System")
    st.caption("💾 **Engine**: SQLite with PostgreSQL Dialect Emulation")
    st.caption("👨‍💻 **Course**: Advanced Relational Database & SQL")

# ---------------------------------------------------------
# GLOBAL TOP KPI RIBBON
# ---------------------------------------------------------
kpis = get_kpis()
occupancy_pct = round(((kpis['booked_seats'] / kpis['total_capacity']) * 100), 1) if kpis['total_capacity'] > 0 else 0

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Total Events</div>
        <div class="kpi-value">{kpis['events']}</div>
        <div class="kpi-tag">Active Schedule</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Venues</div>
        <div class="kpi-value">{kpis['venues']}</div>
        <div class="kpi-tag">5 Major Cities</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Organizers</div>
        <div class="kpi-value">{kpis['organizers']}</div>
        <div class="kpi-tag">Event Producers</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Attendees</div>
        <div class="kpi-value">{kpis['attendees']}</div>
        <div class="kpi-tag">Registered Profiles</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Tickets Sold</div>
        <div class="kpi-value">{kpis['confirmed_tickets']} <span style="font-size:1rem;color:#94A3B8;">/ {kpis['tickets']}</span></div>
        <div class="kpi-tag">Confirmed Bookings</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">₹{kpis['total_revenue']:,.0f}</div>
        <div class="kpi-tag">Realized (Success)</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Avg Ticket Price</div>
        <div class="kpi-value">₹{kpis['avg_ticket_price']:,.0f}</div>
        <div class="kpi-tag">Across All Events</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Seat Occupancy</div>
        <div class="kpi-value">{occupancy_pct}%</div>
        <div class="kpi-tag">{kpis['booked_seats']:,} of {kpis['total_capacity']:,} Seats</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 1: EXECUTIVE DASHBOARD
# ---------------------------------------------------------
if menu == "📊 Executive Dashboard":
    st.subheader("📊 Executive Overview & Operational Performance")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("##### 💰 Realized Revenue per Event (Successful Transactions)")
        query_rev = """
        SELECT e.event_name AS "Event", COALESCE(SUM(p.amount_paid), 0) AS "Revenue (₹)"
        FROM Events e
        LEFT JOIN Tickets t ON e.event_id = t.event_id
        LEFT JOIN Payments p ON t.ticket_id = p.ticket_id AND p.payment_status = 'Success'
        GROUP BY e.event_id, e.event_name
        ORDER BY "Revenue (₹)" DESC;
        """
        df_rev, _, _ = run_query(query_rev)
        if df_rev is not None and not df_rev.empty:
            fig_rev = px.bar(
                df_rev,
                x="Revenue (₹)",
                y="Event",
                orientation='h',
                color="Revenue (₹)",
                color_continuous_scale="Viridis",
                text="Revenue (₹)"
            )
            fig_rev.update_layout(
                yaxis=dict(autorange="reversed"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                margin=dict(l=10, r=10, t=10, b=10),
                height=320
            )
            fig_rev.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
            st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("##### 🎟️ Ticket Booking Status Breakdown")
        query_tix_status = """
        SELECT status AS "Status", COUNT(*) AS "Count"
        FROM Tickets
        GROUP BY status;
        """
        df_tix, _, _ = run_query(query_tix_status)
        if df_tix is not None and not df_tix.empty:
            fig_tix = px.pie(
                df_tix,
                names="Status",
                values="Count",
                hole=0.5,
                color="Status",
                color_discrete_map={
                    "Confirmed": "#10B981",
                    "Pending": "#F59E0B",
                    "Cancelled": "#EF4444"
                }
            )
            fig_tix.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                margin=dict(l=10, r=10, t=10, b=10),
                height=320
            )
            st.plotly_chart(fig_tix, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("##### 🏛️ Venue Capacity vs Event Allocation")
        query_venue = """
        SELECT v.venue_name AS "Venue", v.location AS "City", v.capacity AS "Capacity", COUNT(e.event_id) AS "Scheduled Events"
        FROM Venues v
        LEFT JOIN Events e ON v.venue_id = e.venue_id
        GROUP BY v.venue_id, v.venue_name, v.location, v.capacity
        ORDER BY v.capacity DESC;
        """
        df_venue, _, _ = run_query(query_venue)
        if df_venue is not None and not df_venue.empty:
            fig_venue = px.bar(
                df_venue,
                x="Venue",
                y="Capacity",
                color="City",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                text="Scheduled Events"
            )
            fig_venue.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                margin=dict(l=10, r=10, t=10, b=10),
                height=300
            )
            fig_venue.update_traces(texttemplate='%{text} Events', textposition='inside')
            st.plotly_chart(fig_venue, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("##### 💳 Payment Gateway Statuses")
        query_pay = """
        SELECT payment_status AS "Status", COUNT(*) AS "Transactions", SUM(amount_paid) AS "Amount"
        FROM Payments
        GROUP BY payment_status;
        """
        df_pay, _, _ = run_query(query_pay)
        if df_pay is not None and not df_pay.empty:
            fig_pay = px.bar(
                df_pay,
                x="Status",
                y="Amount",
                color="Status",
                color_discrete_map={
                    "Success": "#10B981",
                    "Pending": "#F59E0B",
                    "Failed": "#EF4444"
                },
                text="Amount"
            )
            fig_pay.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                margin=dict(l=10, r=10, t=10, b=10),
                height=300
            )
            fig_pay.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
            st.plotly_chart(fig_pay, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Event Schedule
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown("##### 📅 Scheduled Events Schedule & Availability")
    query_schedule = """
    SELECT 
        e.event_id AS "ID",
        e.event_name AS "Event Name",
        e.event_date AS "Date & Time",
        v.venue_name AS "Venue",
        v.location AS "City",
        o.organizer_name AS "Organizer",
        e.ticket_price AS "Price (₹)",
        e.total_seats AS "Total Seats",
        e.available_seats AS "Available Seats"
    FROM Events e
    INNER JOIN Venues v ON e.venue_id = v.venue_id
    INNER JOIN Organizers o ON e.organizer_id = o.organizer_id
    ORDER BY e.event_date ASC;
    """
    df_sched, _, _ = run_query(query_schedule)
    if df_sched is not None:
        st.dataframe(df_sched, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 2: DATABASE EXPLORER
# ---------------------------------------------------------
elif menu == "🗄️ Database Explorer":
    st.subheader("🗄️ Database Explorer & Schema Inspector")
    st.markdown("Browse, inspect, and export all 6 normalized relational database tables.")
    
    tables = get_table_names()
    selected_table = st.selectbox("Select a table to inspect:", tables, index=2)
    
    col_t1, col_t2 = st.columns([3, 1])
    
    df_table = get_table_data(selected_table)
    df_schema = get_table_schema(selected_table)
    
    with col_t1:
        st.markdown(f"#### 📋 Table Data: `{selected_table}`")
        st.caption(f"Showing all {len(df_table)} records stored in `{selected_table}`.")
        
        # Search filter
        search_kw = st.text_input(f"🔍 Search within `{selected_table}`:", placeholder="Type to filter rows...")
        if search_kw:
            mask = df_table.astype(str).apply(lambda row: row.str.contains(search_kw, case=False).any(), axis=1)
            display_df = df_table[mask]
        else:
            display_df = df_table
            
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download {selected_table} as CSV",
            data=csv_data,
            file_name=f"{selected_table.lower()}_data.csv",
            mime="text/csv"
        )
        
    with col_t2:
        st.markdown("#### 📐 Schema & Columns")
        st.dataframe(df_schema[["Column Name", "Data Type", "Primary Key"]], use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown(f"**Total Records:** `{len(df_table)}`")
        st.markdown(f"**Total Columns:** `{len(df_schema)}`")

# ---------------------------------------------------------
# MODULE 3: VISUAL ANALYTICS
# ---------------------------------------------------------
elif menu == "📈 Visual Analytics":
    st.subheader("📈 Visual Analytics & Advanced Business Intelligence")
    
    tab1, tab2, tab3 = st.tabs(["💰 Financial & Pricing", "👥 Attendee Demographics", "📊 Demand & Capacity"])
    
    with tab1:
        st.markdown("#### 💵 Ticket Pricing vs. Total Seating Capacity")
        q_scatter = """
        SELECT event_name, ticket_price, total_seats, available_seats,
               (total_seats - available_seats) AS booked_seats,
               ticket_price * (total_seats - available_seats) AS estimated_revenue
        FROM Events;
        """
        df_sc, _, _ = run_query(q_scatter)
        if df_sc is not None:
            fig_sc = px.scatter(
                df_sc,
                x="total_seats",
                y="ticket_price",
                size="booked_seats",
                color="estimated_revenue",
                hover_name="event_name",
                color_continuous_scale="Viridis",
                labels={
                    "total_seats": "Venue Total Capacity",
                    "ticket_price": "Ticket Price (₹)",
                    "estimated_revenue": "Estimated Revenue (₹)",
                    "booked_seats": "Booked Seats"
                }
            )
            fig_sc.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                height=400
            )
            st.plotly_chart(fig_sc, use_container_width=True)

    with tab2:
        st.markdown("#### 👥 Organizer Event Portfolios")
        q_org = """
        SELECT o.organizer_name AS "Organizer", COUNT(e.event_id) AS "Events Managed",
               COALESCE(SUM(p.amount_paid), 0) AS "Total Revenue Generated"
        FROM Organizers o
        LEFT JOIN Events e ON o.organizer_id = e.organizer_id
        LEFT JOIN Tickets t ON e.event_id = t.event_id
        LEFT JOIN Payments p ON t.ticket_id = p.ticket_id AND p.payment_status = 'Success'
        GROUP BY o.organizer_id, o.organizer_name;
        """
        df_org, _, _ = run_query(q_org)
        if df_org is not None:
            fig_org = px.bar(
                df_org,
                x="Organizer",
                y="Total Revenue Generated",
                color="Events Managed",
                color_continuous_scale="Turbo",
                text="Total Revenue Generated"
            )
            fig_org.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                height=380
            )
            fig_org.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
            st.plotly_chart(fig_org, use_container_width=True)

    with tab3:
        st.markdown("#### 📊 Event Demand Classification (CASE Statement Analysis)")
        q_demand = """
        SELECT 
            CASE
                WHEN available_seats < (total_seats * 0.20) THEN 'High Demand (< 20% left)'
                WHEN available_seats < (total_seats * 0.50) THEN 'Moderate Demand (< 50% left)'
                ELSE 'Low Demand (>= 50% left)'
            END AS "Demand Category",
            COUNT(*) AS "Event Count"
        FROM Events
        GROUP BY "Demand Category";
        """
        df_dem, _, _ = run_query(q_demand)
        if df_dem is not None:
            fig_dem = px.pie(
                df_dem,
                names="Demand Category",
                values="Event Count",
                color="Demand Category",
                color_discrete_map={
                    "High Demand (< 20% left)": "#EF4444",
                    "Moderate Demand (< 50% left)": "#F59E0B",
                    "Low Demand (>= 50% left)": "#10B981"
                },
                hole=0.45
            )
            fig_dem.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                height=380
            )
            st.plotly_chart(fig_dem, use_container_width=True)

# ---------------------------------------------------------
# MODULE 4: SQL QUERIES SHOWCASE
# ---------------------------------------------------------
elif menu == "💡 SQL Queries Showcase":
    st.subheader("💡 SQL Queries Showcase & Examination Laboratory")
    st.markdown("Catalog of all exam tasks, analytical joins, nested subqueries, and window functions.")
    
    categories = list(dict.fromkeys([q["category"] for q in PROJECT_QUERIES]))
    selected_cat = st.selectbox("Filter queries by section category:", ["All Categories"] + categories)
    
    if selected_cat != "All Categories":
        filtered_queries = [q for q in PROJECT_QUERIES if q["category"] == selected_cat]
    else:
        filtered_queries = PROJECT_QUERIES
        
    query_titles = [f"{q['question_num']} - {q['title']}" for q in filtered_queries]
    selected_query_title = st.selectbox("Select specific SQL Query to execute:", query_titles)
    
    selected_q = next(q for q in filtered_queries if f"{q['question_num']} - {q['title']}" == selected_query_title)
    
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown(f"### {selected_q['title']}")
    st.markdown(f"**Section:** `{selected_q['category']}` &nbsp;|&nbsp; **Question Ref:** `{selected_q['question_num']}`")
    st.write(selected_q["description"])
    
    # Concept badges
    badges_html = "".join([f'<span class="badge">{concept}</span>' for concept in selected_q["concepts"]])
    st.markdown(badges_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab_sql1, tab_sql2 = st.tabs(["⚡ Executable SQL", "🐘 PostgreSQL Dialect"])
    with tab_sql1:
        st.code(selected_q["sql"], language="sql")
    with tab_sql2:
        st.code(selected_q["pg_sql"], language="sql")
        
    col_btn, col_metric = st.columns([1, 3])
    with col_btn:
        run_btn = st.button("🚀 Execute Query", key=f"btn_{selected_q['id']}", use_container_width=True)
    
    # Run the query
    df_res, exec_time, err = run_query(selected_q["sql"])
    
    if err:
        st.error(f"❌ Execution Error: {err}")
    elif df_res is not None:
        with col_metric:
            st.markdown(f"""
            <div style="padding-top: 5px;">
                <span class="metric-pill">⏱️ Execution Time: {exec_time:.2f} ms</span>
                <span class="metric-pill">🔢 Total Rows: {len(df_res)}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.dataframe(df_res, use_container_width=True, hide_index=True)
        
        # Download button
        csv_export = df_res.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Result CSV",
            data=csv_export,
            file_name=f"query_{selected_q['question_num'].replace('.', '_')}_result.csv",
            mime="text/csv",
            key=f"dl_{selected_q['id']}"
        )
        
        # Auto-visualizer if appropriate
        if selected_q.get("visualize_as") == "bar" and len(df_res) > 0 and len(df_res.columns) >= 2:
            num_cols = df_res.select_dtypes(include=['number']).columns.tolist()
            cat_cols = df_res.select_dtypes(include=['object']).columns.tolist()
            if num_cols and cat_cols:
                with st.expander("📊 View Graphical Visualization", expanded=True):
                    fig = px.bar(
                        df_res,
                        x=cat_cols[0],
                        y=num_cols[-1],
                        color=num_cols[-1],
                        color_continuous_scale="Purples",
                        text=num_cols[-1]
                    )
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font_color="#F8FAFC",
                        margin=dict(l=10, r=10, t=10, b=10)
                    )
                    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# MODULE 5: INTERACTIVE SQL CONSOLE
# ---------------------------------------------------------
elif menu == "⚡ Interactive SQL Console":
    st.subheader("⚡ Interactive SQL Console & Ad-Hoc Query Lab")
    st.markdown("Execute custom SQL queries directly against the database with auto PostgreSQL-to-SQLite translation.")
    
    st.markdown("##### 💡 Quick Sample Queries:")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    
    sample_q = ""
    with col_t1:
        if st.button("📍 Events in Ahmedabad", use_container_width=True):
            st.session_state["custom_sql"] = "SELECT event_name, event_date, ticket_price FROM Events WHERE event_name LIKE '%Ahmedabad%';"
    with col_t2:
        if st.button("🏆 Top Revenue Events", use_container_width=True):
            st.session_state["custom_sql"] = """SELECT e.event_name, SUM(p.amount_paid) AS total_revenue 
FROM Events e 
JOIN Tickets t ON e.event_id = t.event_id 
JOIN Payments p ON t.ticket_id = p.ticket_id AND p.payment_status = 'Success' 
GROUP BY e.event_name 
ORDER BY total_revenue DESC;"""
    with col_t3:
        if st.button("📈 Cumulative Sales", use_container_width=True):
            st.session_state["custom_sql"] = """SELECT ticket_id, booking_date, status, 
COUNT(*) OVER (ORDER BY booking_date) AS cumulative_sales 
FROM Tickets ORDER BY booking_date;"""
    with col_t4:
        if st.button("🎯 High Demand Events", use_container_width=True):
            st.session_state["custom_sql"] = """SELECT event_name, total_seats, available_seats,
CASE WHEN available_seats < (total_seats * 0.2) THEN 'High' ELSE 'Normal' END AS demand
FROM Events;"""

    initial_sql = st.session_state.get("custom_sql", "SELECT * FROM Events LIMIT 5;")
    custom_sql = st.text_area("Write SQL Query:", value=initial_sql, height=130)
    
    col_run, col_clear = st.columns([1, 5])
    with col_run:
        exec_click = st.button("▶ Run SQL", use_container_width=True, type="primary")
        
    if exec_click or custom_sql:
        df_cust, ms, err_cust = run_query(custom_sql)
        if err_cust:
            st.error(f"❌ SQL Execution Error: {err_cust}")
        elif df_cust is not None:
            st.success(f"✅ Success! Executed in {ms:.2f} ms ({len(df_cust)} rows returned)")
            st.dataframe(df_cust, use_container_width=True, hide_index=True)
            
            # Export CSV
            csv_custom = df_cust.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Result as CSV",
                data=csv_custom,
                file_name="custom_query_result.csv",
                mime="text/csv"
            )

# ---------------------------------------------------------
# MODULE 6: DATA MANAGEMENT (CRUD LAB)
# ---------------------------------------------------------
elif menu == "➕ Data Management (CRUD)":
    st.subheader("➕ Data Management & CRUD Administration")
    st.markdown("Perform live inserts, updates, and removals to test referential integrity constraints.")
    
    crud_tab1, crud_tab2, crud_tab3, crud_tab4, crud_tab5 = st.tabs([
        "🎪 New Event",
        "🎟️ Book Ticket",
        "💳 Record Payment",
        "👤 Register Attendee",
        "✏️ Update / Delete"
    ])
    
    with crud_tab1:
        st.markdown("#### 🎪 Schedule New Event")
        with st.form("form_add_event"):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                new_e_id = st.number_input("Event ID", min_value=1, value=12, step=1)
                new_e_name = st.text_input("Event Name", value="Gujarat Tech Innovation Summit")
                new_e_date = st.text_input("Event Date & Time", value="2027-02-15 10:00:00")
                new_e_venue = st.selectbox("Venue", [1, 2, 3, 4, 5, 6], format_func=lambda x: f"Venue #{x}")
            with col_e2:
                new_e_org = st.selectbox("Organizer", [1, 2, 3, 4, 5], format_func=lambda x: f"Organizer #{x}")
                new_e_price = st.number_input("Ticket Price (₹)", min_value=0.0, value=1800.0, step=100.0)
                new_e_seats = st.number_input("Total Capacity Seats", min_value=50, value=1000, step=50)
                new_e_avail = st.number_input("Available Seats", min_value=0, value=1000, step=50)
                
            submitted_event = st.form_submit_button("Add Event")
            if submitted_event:
                try:
                    add_event(new_e_id, new_e_name, new_e_date, new_e_venue, new_e_org, new_e_price, new_e_seats, new_e_avail)
                    st.success(f"Event '{new_e_name}' successfully scheduled!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding event: {e}")

    with crud_tab2:
        st.markdown("#### 🎟️ Book Event Ticket")
        with st.form("form_book_ticket"):
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                t_id = st.number_input("Ticket ID", min_value=1, value=16, step=1)
                t_event = st.number_input("Event ID", min_value=1, value=1, step=1)
                t_attendee = st.number_input("Attendee ID", min_value=1, value=4, step=1)
            with col_b2:
                t_date = st.text_input("Booking Date", value="2026-08-09 14:00:00")
                t_status = st.selectbox("Booking Status", ["Confirmed", "Pending", "Cancelled"])
                
            book_submitted = st.form_submit_button("Confirm Booking")
            if book_submitted:
                try:
                    book_ticket(t_id, t_event, t_attendee, t_date, t_status)
                    st.success(f"Ticket #{t_id} successfully booked with status {t_status}!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error booking ticket: {e}")

    with crud_tab3:
        st.markdown("#### 💳 Record Payment Transaction")
        with st.form("form_record_pay"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                p_id = st.number_input("Payment ID", min_value=1, value=16, step=1)
                p_t_id = st.number_input("Ticket ID Reference", min_value=1, value=16, step=1)
                p_amount = st.number_input("Amount Paid (₹)", min_value=0.0, value=1500.0, step=100.0)
            with col_p2:
                p_status = st.selectbox("Payment Status", ["Success", "Pending", "Failed"])
                p_date = st.text_input("Payment Timestamp", value="2026-08-09 14:05:00")
                
            pay_submitted = st.form_submit_button("Submit Payment Record")
            if pay_submitted:
                try:
                    record_payment(p_id, p_t_id, p_amount, p_status, p_date)
                    st.success(f"Payment #{p_id} recorded with status {p_status}!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error recording payment: {e}")

    with crud_tab4:
        st.markdown("#### 👤 Register New Attendee")
        with st.form("form_register_attendee"):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                a_id = st.number_input("Attendee ID", min_value=1, value=13, step=1)
                a_name = st.text_input("Full Name", value="Sunita Rao")
            with col_a2:
                a_email = st.text_input("Email Address", value="sunita@gmail.com")
                a_phone = st.text_input("Phone Number", value="9000000013")
                
            att_submitted = st.form_submit_button("Register Attendee")
            if att_submitted:
                try:
                    add_attendee(a_id, a_name, a_email, a_phone)
                    st.success(f"Attendee '{a_name}' registered successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error registering attendee: {e}")

    with crud_tab5:
        st.markdown("#### ✏️ Update Ticket Price or Delete Event")
        col_u, col_d = st.columns(2)
        with col_u:
            st.markdown("##### Update Ticket Price")
            u_event_id = st.number_input("Event ID to Update", min_value=1, value=1, step=1)
            u_new_price = st.number_input("New Ticket Price (₹)", min_value=0.0, value=1750.0, step=50.0)
            if st.button("Update Price"):
                try:
                    update_ticket_price(u_event_id, u_new_price)
                    st.success(f"Event #{u_event_id} price updated to ₹{u_new_price}!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating price: {e}")

        with col_d:
            st.markdown("##### Delete Event Record")
            d_event_id = st.number_input("Event ID to Delete", min_value=1, value=11, step=1)
            if st.button("Delete Event", type="secondary"):
                try:
                    delete_event(d_event_id)
                    st.warning(f"Event #{d_event_id} deleted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting event: {e}")

# ---------------------------------------------------------
# MODULE 7: RELATIONAL SCHEMA & ER DIAGRAM
# ---------------------------------------------------------
elif menu == "🏗️ Relational Schema & ER":
    st.subheader("🏗️ Relational Database Architecture & Integrity Constraints")
    st.markdown("Comprehensive relational diagram, keys, custom types, and entity relationships.")
    
    st.markdown("""
    ```mermaid
    erDiagram
        VENUES ||--o{ EVENTS : hosts
        ORGANIZERS ||--o{ EVENTS : manages
        EVENTS ||--o{ TICKETS : issues
        ATTENDEES ||--o{ TICKETS : books
        TICKETS ||--o{ PAYMENTS : generates

        VENUES {
            int venue_id PK
            string venue_name
            string location
            int capacity
        }

        ORGANIZERS {
            int organizer_id PK
            string organizer_name
            string contact_email
            string phone_number
        }

        EVENTS {
            int event_id PK
            string event_name
            timestamp event_date
            int venue_id FK
            int organizer_id FK
            decimal ticket_price
            int total_seats
            int available_seats
        }

        ATTENDEES {
            int attendee_id PK
            string name
            string email
            string phone_number
        }

        TICKETS {
            int ticket_id PK
            int event_id FK
            int attendee_id FK
            timestamp booking_date
            string status "Confirmed | Cancelled | Pending"
        }

        PAYMENTS {
            int payment_id PK
            int ticket_id FK
            decimal amount_paid
            string payment_status "Success | Failed | Pending"
            timestamp payment_date
        }
    ```
    """)
    
    st.markdown("---")
    st.markdown("#### 🔒 Integrity Constraints Summary")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("""
        * **Primary Keys (PK):**
          - `Venues.venue_id`
          - `Organizers.organizer_id`
          - `Events.event_id`
          - `Attendees.attendee_id`
          - `Tickets.ticket_id`
          - `Payments.payment_id`
        * **Foreign Keys (FK):**
          - `Events.venue_id` ➔ `Venues.venue_id`
          - `Events.organizer_id` ➔ `Organizers.organizer_id`
          - `Tickets.event_id` ➔ `Events.event_id`
          - `Tickets.attendee_id` ➔ `Attendees.attendee_id`
          - `Payments.ticket_id` ➔ `Tickets.ticket_id`
        """)
    with col_c2:
        st.markdown("""
        * **Unique Constraints:**
          - `UNIQUE (event_id, attendee_id)` on `Tickets`: Guarantees an attendee cannot book duplicate tickets for the same event.
        * **Status Enumerations (ENUM / CHECK):**
          - `ticket_status_type`: `'Confirmed'`, `'Cancelled'`, `'Pending'`
          - `payment_status_type`: `'Success'`, `'Failed'`, `'Pending'`
        * **Referential Integrity:** Enforced cascading validation across ticket generation and financial transactions.
        """)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 12px 0;">
    🎭 Event Management System SQL Portal • Built with Streamlit, Plotly & SQLite / PostgreSQL Engine • Complete Examination Solution
</div>
""", unsafe_allow_html=True)
