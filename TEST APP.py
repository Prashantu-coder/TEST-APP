# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Setup ---
st.set_page_config(page_title="Quantexo", layout="wide")

# Custom CSS for light black theme
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a;
    }
    .stSelectbox, .stTextInput, .stButton>button {
        background-color: #2d2d2d !important;
        color: white !important;
        border-color: #444 !important;
    }
    .header-container {
        color: white;
        padding: 1rem;
        background-color: #1a1a1a;
        border-bottom: 1px solid #444;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .header-subtitle {
        font-size: 1.2rem;
        color: #aaa;
    }
    </style>
    <div class='header-container'>
        <div class='header-title'>Quantexo🕵️</div>
        <div class='header-subtitle'>💰 Advanced Insights for Bold Trades</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Company Search ---
companies = {"ACLBSL", "ADBL", "AHL", "AHPC", "AKJCL", "AKPL", "ALBSL", "ALICL", "ANLB", "API", "AVYAN", "BARUN", "BBC", "BEDC", "BFC", "BGWT", "BHDC", "BHL", "BHPL", "BNHC", "BNL", "BNT", "BPCL", "C30MF", "CBBL", "CCBD88", "CFCL", "CGH", "CHCL", "CHDC", "CHL", "CIT", "CITY", "CIZBD90", "CKHL", "CLI", "CMF2", "CORBL", "CREST", "CYCL", "CZBIL", "DDBL", "DHPL", "DLBS", "DOLTI", "DORDI", "EBL", "EBLD85", "EBLD86", "EDBL", "EHPL", "ENL", "FMDBL", "FOWAD", "GBBD85", "GBBL", "GBILD84/85", "GBILD86/87", "GBIME", "GBLBS", "GCIL", "GFCL", "GHL", "GIBF1", "GILB", "GLBSL", "GLH", "GMFBS", "GMFIL", "GMLI", "GRDBL", "GSY", "GUFL", "GVL", "GWFD83", "H8020", "HATHY", "HBL", "HDHPC", "HDL", "HEI", "HEIP", "HHL", "HIDCL", "HIDCLP", "HLBSL", "HLI", "HPPL", "HRL", "HURJA", "ICFC", "ICFCD83", "ICFCD88", "IGI", "IHL", "ILBS", "ILI", "JBBD87", "JBBL", "JBBLPO", "JBLB", "JFL", "JOSHI", "JSLBB", "KBL", "KBLD86", "KBSH", "KDBY", "KDL", "KEF", "KKHC", "KMCDB", "KPCL", "KSBBL", "KSBBLD87", "KSY", "LBBL", "LEC", "LICN", "LLBS", "LSL", "LUK", "LVF2", "MAKAR", "MANDU", "MATRI", "MBJC", "MBL", "MBLD87", "MCHL", "MDB", "MEHL", "MEL", "MEN", "MERO", "MFIL", "MFLD85", "MHCL", "MHL", "MHNL", "MKCL", "MKHC", "MKHL", "MKJC", "MLBBL", "MLBL", "MLBS", "MLBSL", "MMF1", "MMKJL", "MNBBL", "MNMF1", "MPFL", "MSHL", "MSLB", "NABBC", "NABIL", "NABILD87", "NADEP", "NBBD2085", "NBF2", "NBF3", "NBL", "NBLD85", "NBLD87", "NESDO", "NFS", "NGPL", "NHDL", "NHPC", "NIBD2082", "NIBD84", "NIBLGF", "NIBLSTF", "NIBSF2", "NICA", "NICBF", "NICD88", "NICFC", "NICGF2", "NICL", "NICLBSL", "NICSF", "NIFRA", "NIFRAUR85/86", "NIL", "NIMB", "NIMBPO", "NLG", "NLIC", "NLICL", "NMB", "NMB50", "NMBHF2", "NMBMF", "NMFBS", "NMIC", "NMLBBL", "NRIC", "NRM", "NRN", "NSIF2", "NTC", "NUBL", "NWCL", "NYADI", "OHL", "OMPL", "PBD84", "PBD88", "PCBL", "PFL", "PHCL", "PMHPL", "PMLI", "PPCL", "PPL", "PRIN", "PROFL", "PRSF", "PRVU", "PSF", "RADHI", "RAWA", "RBCL", "RBCLPO", "RFPL", "RHGCL", "RHPL", "RIDI", "RLFL", "RMF1", "RMF2", "RNLI", "RSDC", "RURU", "SADBL", "SAGF", "SAHAS", "SALICO", "SAMAJ", "SAND2085", "SANIMA", "SAPDBL", "SARBTM", "SBCF", "SBD87", "SBI", "SBID83", "SBID89", "SBL", "SCB", "SEF", "SFCL", "SFEF", "SFMF", "SGHC", "SGIC", "SHEL", "SHINE", "SHIVM", "SHL", "SHLB", "SHPC", "SICL", "SIFC", "SIGS3", "SIKLES", "SINDU", "SJCL", "SJLIC", "SKBBL", "SLBBL", "SLBSL", "SLCF", "SMATA", "SMB", "SMFBS", "SMH", "SMHL", "SMJC", "SMPDA", "SNLI", "SONA", "SPC", "SPDL", "SPHL", "SPIL", "SPL", "SRLI", "SSHL", "STC", "SWBBL", "SWMF", "TAMOR", "TPC", "TRH", "TSHL", "TVCL", "UAIL", "UHEWA", "ULBSL", "ULHC", "UMHL", "UMRH", "UNHPL", "UNLB", "UPCL", "UPPER", "USHEC", "USHL", "USLB", "VLBS", "VLUCL", "WNLB"}

col1, col2, col3 = st.columns([1,1,1.2])
with col1:
    selected_dropdown = st.selectbox("",options=[""] + sorted(list(companies)), index=0, label_visibility="collapsed")
with col2: 
    user_input = st.text_input("🔍 Enter Company Symbol","", label_visibility="collapsed",placeholder="🔍 Enter Company Symbol")
with col3: search_clicked = st.button("Search")

# --- Priority: Manual Entry overrides Dropdown ---
if search_clicked:
    if user_input.strip():
        company_symbol = user_input.strip().upper()
    elif selected_dropdown:
        company_symbol = selected_dropdown
    else:
        st.warning("⚠️ Please enter or select a company.")
        company_symbol = ""
else:
    company_symbol = ""

if company_symbol:
    @st.cache_data(ttl=3600)
    def get_sheet_data(symbol, sheet_name="Daily Price"):
        try:
            # Google Sheets URL with the specific sheet's gid
            sheet_url = f"https://docs.google.com/spreadsheets/d/1Q_En7VGGfifDmn5xuiF-t_02doPpwl4PLzxb4TBCW0Q/export?format=csv&gid={get_sheet_gid(sheet_name)}"
            
            # Read data as CSV directly (no auth needed if public)
            df = pd.read_csv(sheet_url)

            # Ensure only the first 7 columns are used (ignoring any additional columns)
            df = df.iloc[:, :7]  # Select only the first 7 columns

            # Define the columns based on the new column mappings
            df.columns = ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']

            # Filter data based on company symbol
            df['symbol'] = df['symbol'].astype(str).str.strip().str.upper()
            return df[df['symbol'].str.upper() == symbol.upper()]
        except Exception as e:
            st.error(f"🔴 Error fetching data: {str(e)}")
            return pd.DataFrame()

    def get_sheet_gid(sheet_name):
        # You need to know the gid value of the sheet, or you can find it in the sheet's URL when editing the sheet
        sheet_gids = {
            "Daily Price": 0,  # Default sheet (GID of Sheet1)
        }
        return sheet_gids.get(sheet_name, 0)

    sheet_name = "Daily Price"
    df = get_sheet_data(company_symbol, sheet_name)

    if df.empty:
        st.warning(f"No data found for {company_symbol}")
        st.stop()

    try:
        # Convert column names to lowercase
        df.columns = [col.lower() for col in df.columns]

        # Check required columns
        required_cols = {'date', 'open', 'high', 'low', 'close', 'volume'}
        if not required_cols.issubset(set(df.columns)):
            st.error("❌ Missing required columns: date, open, high, low, close, volume")
            st.stop()

        # Convert and validate dates
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        if df['date'].isnull().any():
            st.error("❌ Invalid date format in some rows")
            st.stop()

        # Validate numeric columns
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_cols:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace('[^\d.]', '', regex=True),
                errors='coerce'
            )
            if df[col].isnull().any():
                bad_rows = df[df[col].isnull()][['date', col]].head()
                st.error(f"❌ Found {df[col].isnull().sum()} invalid values in {col} column. Examples:")
                st.dataframe(bad_rows)
                st.stop()

        # Remove any rows with NA values
        df = df.dropna()
        if len(df) == 0:
            st.error("❌ No valid data after cleaning")
            st.stop()

        # Sort and reset index
        df.sort_values('date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # Calculate 5 months ago from the last date
        last_date = df['date'].max()
        five_months_ago = last_date - pd.DateOffset(months=5)
        
        # Create slider for date range selection
        min_date = df['date'].min().to_pydatetime()
        max_date = df['date'].max().to_pydatetime()
        
        # Default to showing last 5 months initially
        default_start = max(five_months_ago.to_pydatetime(), min_date)
        
        date_range = st.slider(
            "Select Date Range:",
            min_value=min_date,
            max_value=max_date,
            value=(default_start, max_date),
            format="YYYY-MM-DD"
        )
        
        # Filter data based on selected date range
        filtered_df = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]
        
        # Calculate signals only for filtered data
        filtered_df['point_change'] = filtered_df['close'].diff().fillna(0)
        filtered_df['tag'] = ''
        
        # Dynamically adjust the rolling window size based on available data
        min_window = min(20, max(5, len(filtered_df) // 2))
        
        # Calculate rolling average with adjusted window size
        avg_volume = filtered_df['volume'].rolling(window=min_window).mean()
        
        if avg_volume.notna().sum() > 0:
            avg_volume = avg_volume.fillna(method='bfill').fillna(filtered_df['volume'].mean())
            
            for i in range(min(3, len(filtered_df)-1), len(filtered_df)):
                row = filtered_df.iloc[i]
                prev = filtered_df.iloc[i - 1]
                next_candles = filtered_df.iloc[i + 1:min(i + 6, len(filtered_df))]
                is_last_candle = (i == len(filtered_df) - 1)

                body = abs(row['close'] - row['open'])
                prev_body = abs(prev['close'] - prev['open'])
                recent_tags = filtered_df['tag'].iloc[max(0, i - 4):i]

                # --- Signals ---
                if (
                    row['close'] > row['open'] and
                    row['close'] >= row['high'] - (row['high'] - row['low']) * 0.1 and
                    row['volume'] > avg_volume[i] * 1.5 and
                    body > prev_body and
                    '🟢' not in recent_tags.values
                ):
                    filtered_df.at[i, 'tag'] = '🟢'

                elif (
                    row['open'] > row['close'] and
                    row['close'] <= row['low'] + (row['high'] - row['low']) * 0.1 and
                    row['volume'] > avg_volume[i] * 1.5 and
                    body > prev_body and
                    '🔴' not in recent_tags.values
                ):
                    filtered_df.at[i, 'tag'] = '🔴'

                elif (
                    i >= 10 and
                    row['high'] > max(filtered_df['high'].iloc[i - 10:i]) and
                    row['volume'] > avg_volume[i] * 1.8
                ):
                    if not (filtered_df['tag'].iloc[i - 3:i] == '💥').any():
                        filtered_df.at[i, 'tag'] = '💥'

                elif (
                    i >= 10 and
                    row['low'] < min(filtered_df['low'].iloc[i - 10:i]) and
                    row['volume'] > avg_volume[i] * 1.8
                ):
                    if not (filtered_df['tag'].iloc[i - 3:i] == '💣').any():
                        filtered_df.at[i, 'tag'] = '💣'

                elif (
                    row['close'] > row['open'] and
                    body > (row['high'] - row['low']) * 0.7 and
                    row['volume'] > avg_volume[i] * 2
                ):
                    filtered_df.at[i, 'tag'] = '🐂'

                elif (
                    row['open'] > row['close'] and
                    body > (row['high'] - row['low']) * 0.7 and
                    row['volume'] > avg_volume[i] * 2
                ):
                    filtered_df.at[i, 'tag'] = '🐻'

                elif (
                    filtered_df['point_change'].iloc[i] > 0 and
                    row['close'] > row['open'] and
                    body < 0.3 * prev_body and
                    row['volume'] < avg_volume[i] * 0.5
                ):
                    filtered_df.at[i, 'tag'] = '📉'

                elif (
                    filtered_df['point_change'].iloc[i] < 0 and
                    row['open'] > row['close'] and
                    body < 0.3 * prev_body and
                    row['volume'] < avg_volume[i] * 0.5
                ):
                    filtered_df.at[i, 'tag'] = '📈'

                # Last candle handling
                if is_last_candle:
                    if (
                        row['close'] > row['open'] and
                        row['volume'] > avg_volume[i] * 1.5
                    ):
                        filtered_df.at[i, 'tag'] = '⛔ (Potential)'
                    elif (
                        row['open'] > row['close'] and
                        row['volume'] > avg_volume[i] * 1.5
                    ):
                        filtered_df.at[i, 'tag'] = '🚀 (Potential)'
                else:
                    if (
                        row['close'] > row['open'] and
                        row['volume'] > avg_volume[i] * 1.2
                    ):
                        filtered_df.loc[filtered_df['tag'] == '⛔', 'tag'] = ''
                        for j, candle in next_candles.iterrows():
                            if candle['close'] < row['open']:
                                filtered_df.at[j, 'tag'] = '⛔'
                                break

                    elif (
                        row['open'] > row['close'] and
                        row['volume'] > avg_volume[i] * 1.2
                    ):
                        filtered_df.loc[filtered_df['tag'] == '🚀', 'tag'] = ''
                        for j, candle in next_candles.iterrows():
                            if candle['close'] > row['open']:
                                filtered_df.at[j, 'tag'] = '🚀'
                                break

            # --- Visualization ---
            tag_labels = {
                '🟢': '🟢 Aggressive Buyers',
                '🔴': '🔴 Aggressive Sellers',
                '⛔': '⛔ Buyer Absorption',
                '🚀': '🚀 Seller Absorption',
                '💥': '💥 Bullish POR',
                '💣': '💣 Bearish POR',
                '🐂': '🐂 Bullish POI',
                '🐻': '🐻 Bearish POI',
                '📉': '📉 Bullish Weak Legs',
                '📈': '📈 Bearish Weak Legs'
            }

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=filtered_df['date'], y=filtered_df['close'],
                mode='lines', name='Close Price',
                line=dict(color='#4CAF50', width=2),  # Green line for close price
                customdata=filtered_df[['date', 'open', 'high', 'low', 'close', 'point_change']],
                hovertemplate=(
                    "📅 Date: %{customdata[0]|%Y-%m-%d}<br>" +
                    "🟢 Open: %{customdata[1]:.2f}<br>" +
                    "📈 High: %{customdata[2]:.2f}<br>" +
                    "📉 Low: %{customdata[3]:.2f}<br>" +
                    "💰 LTP: %{customdata[4]:.2f}<br>" +
                    "📊 Point Change: %{customdata[5]:.2f}<extra></extra>"
                )
            ))  

            signals = filtered_df[filtered_df['tag'] != '']
            for tag in signals['tag'].unique():
                subset = signals[signals['tag'] == tag]
                fig.add_trace(go.Scatter(
                    x=subset['date'], y=subset['close'],
                    mode='markers+text',
                    name=tag_labels.get(tag, tag),
                    text=[tag] * len(subset),
                    textposition='top center',
                    textfont=dict(size=20),
                    marker=dict(size=14, symbol="circle", color='white'),
                    customdata=subset[['open', 'high', 'low', 'close', 'point_change']].values,
                    hovertemplate=(
                        "📅 Date: %{x|%Y-%m-%d}<br>" +
                        "🟢 Open: %{customdata[0]:.2f}<br>" +
                        "📈 High: %{customdata[1]:.2f}<br>" +
                        "📉 Low: %{customdata[2]:.2f}<br>" +
                        "🔚 Close: %{customdata[3]:.2f}<br>" +
                        "📊 Point Change: %{customdata[4]:.2f}<br>" +
                        f"{tag_labels.get(tag, tag)}<extra></extra>"
                    )
                ))
                
            # Extend x-axis slightly beyond last date
            extended_date = filtered_df['date'].max() + timedelta(days=15)
            
            fig.update_layout(
                height=800,
                width=1800,
                plot_bgcolor="#2d2d2d",  # Darker background for chart
                paper_bgcolor="#1a1a1a",  # Matching the app background
                font_color="white",
                xaxis=dict(
                    title="Date",
                    tickangle=-45,
                    showgrid=False,
                    range=[filtered_df['date'].min(), extended_date],
                    gridcolor="#444",
                    linecolor="#444",
                    zerolinecolor="#444"
                ),
                yaxis=dict(
                    title="Price",
                    showgrid=True,
                    gridcolor="#444",
                    zeroline=True,
                    zerolinecolor="#444",
                    linecolor="#444"
                ),
                margin=dict(l=50, r=50, b=130, t=50),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=14),
                    bgcolor="rgba(0,0,0,0)"
                ),
                dragmode="zoom",
                annotations=[
                    dict(
                        text=f"{company_symbol} <br> Quantexo",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor="center", yanchor="middle",
                        font=dict(size=25, color="rgba(100, 100, 100, 0.3)"),
                        showarrow=False
                    )
                ]
            )
            
            st.plotly_chart(fig, use_container_width=False)
            
        else:
            st.warning("⚠️ Unable to calculate trading signals due to insufficient data")
            
    except Exception as e:
        st.error(f"⚠️ Processing error: {str(e)}")

else:
    st.info("ℹ👆🏻 Enter a company symbol to get analysed chart 👆🏻")