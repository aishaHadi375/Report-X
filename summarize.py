import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class TrendAnalyzer:
    """Analyzes trends and creates business-friendly visualizations"""

    def __init__(self, df, column_types):
        self.df = df
        self.column_types = column_types

        self.numeric_cols = [
            col for col, dtype in column_types.items()
            if dtype in ["integer", "float"]
        ]

        self.categorical_cols = [
            col for col, dtype in column_types.items()
            if dtype in ["categorical", "boolean", "text"]
        ]

        self.datetime_cols = [
            col for col, dtype in column_types.items()
            if dtype == "datetime"
        ]

    def analyze_trends(self):
        """Perform comprehensive trend analysis"""
        return {
            "numeric_trends": self._analyze_numeric_trends(),
            "categorical_distributions": self._analyze_categorical_distributions(),
            "correlations": self._analyze_correlations(),
            "time_series": self._analyze_time_series(),
            "summary_stats": self._get_summary_statistics(),
        }

    def _analyze_numeric_trends(self):
        """Analyze numeric column trends"""
        trends = {}

        for col in self.numeric_cols[:5]:
            data = self.df[col].dropna()
            if len(data) == 0:
                continue

            mean_val = data.mean()

            trends[col] = {
                "mean": float(mean_val),
                "median": float(data.median()),
                "std": float(data.std()),
                "min": float(data.min()),
                "max": float(data.max()),
                "range": float(data.max() - data.min()),
                "trend_direction": self._detect_trend_direction(data),
                "coefficient_of_variation": float(
                    (data.std() / mean_val) * 100
                ) if mean_val != 0 else 0.0,
            }

        return trends

    def _detect_trend_direction(self, series):
        """Detect if series is increasing, decreasing, or stable"""
        if len(series) < 2:
            return "insufficient_data"

        mid = len(series) // 2
        first_half_mean = series.iloc[:mid].mean()
        second_half_mean = series.iloc[mid:].mean()

        if second_half_mean > first_half_mean * 1.1:
            return "increasing"
        elif second_half_mean < first_half_mean * 0.9:
            return "decreasing"
        else:
            return "stable"

    def _analyze_categorical_distributions(self):
        """Analyze categorical column distributions"""
        distributions = {}

        for col in self.categorical_cols[:3]:
            value_counts = self.df[col].value_counts()

            distributions[col] = {
                "unique_count": int(self.df[col].nunique()),
                "top_values": value_counts.head(5).to_dict(),
                "most_common": str(value_counts.index[0]),
                "most_common_count": int(value_counts.iloc[0]),
                "concentration": float(
                    value_counts.iloc[0] / len(self.df) * 100
                ),
            }

        return distributions

    def _analyze_correlations(self):
        """Find strong correlations between numeric columns"""
        if len(self.numeric_cols) < 2:
            return {}

        corr_matrix = self.df[self.numeric_cols].corr()
        correlations = {}

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]

                if abs(corr_value) > 0.7:
                    pair = f"{corr_matrix.columns[i]} & {corr_matrix.columns[j]}"
                    correlations[pair] = {
                        "coefficient": float(corr_value),
                        "strength": (
                            "strong positive"
                            if corr_value > 0
                            else "strong negative"
                        ),
                    }

        return correlations

    def _analyze_time_series(self):
        """Analyze time-based trends if datetime columns exist"""
        if not self.datetime_cols:
            return {}

        time_analysis = {}

        for col in self.datetime_cols[:1]:
            try:
                date_series = pd.to_datetime(self.df[col])
                time_analysis[col] = {
                    "start_date": str(date_series.min()),
                    "end_date": str(date_series.max()),
                    "span_days": int(
                        (date_series.max() - date_series.min()).days
                    ),
                    "has_trend": True,
                }
            except Exception:
                continue

        return time_analysis

    def _get_summary_statistics(self):
        """Get overall data summary"""
        total_cells = len(self.df) * len(self.df.columns)

        return {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "numeric_columns": len(self.numeric_cols),
            "categorical_columns": len(self.categorical_cols),
            "datetime_columns": len(self.datetime_cols),
            "missing_data_pct": float(
                (self.df.isnull().sum().sum() / total_cells) * 100
            ),
        }

    # --- VISUALIZATION METHODS ---

    def visualize_numeric_distributions(self, top_n=3):
        """Create histograms for top numeric columns"""
        if not self.numeric_cols:
            return None, "No numeric columns found for distribution analysis."

        cols_to_plot = self.numeric_cols[:top_n]

        fig = make_subplots(
            rows=1,
            cols=len(cols_to_plot),
            subplot_titles=[col.replace('_', ' ').title() for col in cols_to_plot],
        )

        for idx, col in enumerate(cols_to_plot, start=1):
            data = self.df[col].dropna()
            fig.add_trace(
                go.Histogram(
                    x=data,
                    name=col,
                    marker_color='skyblue',
                    opacity=0.7,
                ),
                row=1,
                col=idx,
            )

        fig.update_layout(
            title="Distribution of Key Numeric Variables",
            showlegend=False,
            height=400,
        )

        trends = self._analyze_numeric_trends()
        col_name = cols_to_plot[0].replace('_', ' ').title()
        if cols_to_plot[0] in trends:
            info = trends[cols_to_plot[0]]
            insight = f"""📊 **What This Chart Shows:**\n
This histogram shows how your numeric values are spread out.\n
🎯 **Key Findings for '{col_name}':**
• **Average Value:** {info['mean']:.2f}
• **Most Common Range:** Around {info['median']:.2f}
• **Value Spread:** From {info['min']:.2f} to {info['max']:.2f}
• **Trend:** Values are **{info['trend_direction']}**
"""
            if info['trend_direction'] == 'increasing':
                insight += "• Great news! This metric is growing over time, indicating positive momentum\n"
            elif info['trend_direction'] == 'decreasing':
                insight += "• ⚠️ This metric is declining - may need investigation\n"
            else:
                insight += "• This metric is stable - consistent performance\n"
            
            if info['coefficient_of_variation'] > 50:
                insight += "• Values vary significantly - high unpredictability"
            else:
                insight += "• Values are fairly consistent - good predictability"
        else:
            insight = f"📊 Showing distributions for {len(cols_to_plot)} key metrics."

        return fig, insight

    def visualize_categorical_distribution(self):
        """Create bar chart for top categorical column"""
        if not self.categorical_cols:
            return None, "No categorical columns found."

        col = self.categorical_cols[0]
        value_counts = self.df[col].value_counts().head(10)

        fig = go.Figure(
            data=[
                go.Bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    text=value_counts.values,
                    textposition="auto",
                    marker_color='lightcoral'
                )
            ]
        )

        fig.update_layout(
            title=f"Distribution of '{col.replace('_', ' ').title()}'",
            xaxis_title=col.replace('_', ' ').title(),
            yaxis_title="Count",
            height=400,
        )

        distributions = self._analyze_categorical_distributions()
        dist_info = distributions.get(col)

        if dist_info:
            insight = f"""📊 **What This Chart Shows:**\n
This bar chart displays the frequency of different categories in your '{col.replace('_', ' ').title()}' field.\n
🎯 **Key Findings:**
• **Total Categories:** {dist_info['unique_count']} different types
• **Most Common:** '{dist_info['most_common']}' appears {dist_info['most_common_count']} times
• **Concentration:** {dist_info['concentration']:.1f}% of records are in the top category
"""
            if dist_info['concentration'] > 70:
                insight += f"• ⚠️ Heavy concentration in '{dist_info['most_common']}' - consider diversification"
            elif dist_info['concentration'] < 20:
                insight += "• ✅ Well-balanced distribution across categories"
            else:
                insight += "• Moderate concentration - reasonable balance"
        else:
            insight = f"Showing top 10 categories in '{col.replace('_', ' ').title()}'"

        return fig, insight

    def visualize_trend_summary(self):
        """Create summary metrics visualization"""
        trends = self._analyze_numeric_trends()

        if not trends:
            return None, "No numeric data available for trend summary."

        metrics_data = []
        for col, info in list(trends.items())[:4]:
            trend_emoji = "📈" if info['trend_direction'] == 'increasing' else "📉" if info['trend_direction'] == 'decreasing' else "➡️"
            metrics_data.append([
                col.replace('_', ' ').title(),
                f"{info['mean']:.2f}",
                f"{info['median']:.2f}",
                f"{info['range']:.2f}",
                f"{trend_emoji} {info['trend_direction'].title()}",
            ])

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=[
                            "<b>Metric</b>",
                            "<b>Average</b>",
                            "<b>Median</b>",
                            "<b>Range</b>",
                            "<b>Trend</b>",
                        ],
                        fill_color="paleturquoise",
                        align="left",
                        font=dict(size=12, color='black')
                    ),
                    cells=dict(
                        values=list(zip(*metrics_data)),
                        fill_color="lavender",
                        align="left",
                        font=dict(size=11)
                    ),
                )
            ]
        )

        fig.update_layout(
            title="Quick Metrics Summary",
            height=300,
        )

        inc = sum(1 for v in trends.values() if v["trend_direction"] == "increasing")
        dec = sum(1 for v in trends.values() if v["trend_direction"] == "decreasing")
        stab = sum(1 for v in trends.values() if v["trend_direction"] == "stable")

        insight = f"""📊 **What This Table Shows:**\n
A quick summary of your key metrics with their performance trends.\n
🎯 **Overall Trend Status:**
• **{inc} metrics growing** 📈 - Good momentum
• **{dec} metrics declining** 📉 - Need attention
• **{stab} metrics stable** ➡️ - Consistent performance
"""

        if inc > dec:
            insight += "• Overall positive trend - business is moving in right direction"
        elif dec > inc:
            insight += "• ⚠️ More declining than growing metrics - review declining areas"
        else:
            insight += "• Mixed trends - some areas growing while others need attention"

        return fig, insight

    # --- CORRELATION PIE CHART ---
    def visualize_correlation_pie(self):
        """Create pie chart showing proportion of strong/weak correlations"""
        if len(self.numeric_cols) < 2:
            return None, "Need at least 2 numeric columns for correlation analysis."

        corr_matrix = self.df[self.numeric_cols[:8]].corr()
        strong_pos, strong_neg, weak = 0, 0, 0

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if corr_value > 0.7:
                    strong_pos += 1
                elif corr_value < -0.7:
                    strong_neg += 1
                else:
                    weak += 1

        labels = ["Strong Positive", "Strong Negative", "Weak/No Correlation"]
        values = [strong_pos, strong_neg, weak]
        colors = ["#1f77b4", "#ff7f0e", "#d3d3d3"]

        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                textinfo='label+percent',
                marker=dict(colors=colors),
                hole=0.4
            )]
        )

        fig.update_layout(
            title="Overview of Metric Relationships",
            height=400,
        )

        insight = f"""📊 **What This Pie Chart Shows:**\n
This chart summarizes how your key numeric metrics relate to each other.\n
🎯 **Key Findings:**
• **Strong Positive Correlations:** {strong_pos} pairs (move together)
• **Strong Negative Correlations:** {strong_neg} pairs (move opposite)
• **Weak/No Correlations:** {weak} pairs (largely independent)\n
💡 **What This Means for Your Business:**
• Focus on strongly correlated metrics for strategy alignment
• Weakly correlated metrics can be analyzed independently
"""

        return fig, insight

    # --- WRAPPER METHODS ---
    def create_distribution_chart_with_explanation(self):
        return self.visualize_numeric_distributions()
    
    def create_categorical_chart_with_explanation(self):
        return self.visualize_categorical_distribution()

    def create_correlation_chart_with_explanation(self):
        return self.visualize_correlation_pie()
