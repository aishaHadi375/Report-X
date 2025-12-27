"""
Interactive Data Explorer - Let users ask questions about their data
"""

import plotly.express as px
import plotly.graph_objects as go

class InteractiveExplorer:
    """Allow users to explore data through natural queries"""
    
    def __init__(self, df, column_types):
        self.df = df
        self.column_types = column_types
        self.numeric_cols = [col for col, dtype in column_types.items() 
                            if dtype in ["integer", "float"]]
        self.categorical_cols = [col for col, dtype in column_types.items() 
                                if dtype in ["categorical", "boolean", "text"]]
    
    def create_custom_comparison(self, metric1, metric2, chart_type="scatter"):
        """Create custom comparison charts"""
        
        if chart_type == "scatter":
            fig = px.scatter(
                self.df,
                x=metric1,
                y=metric2,
                title=f"{metric1.replace('_', ' ').title()} vs {metric2.replace('_', ' ').title()}",
                trendline="ols"
            )
            
            insight = f"""
**Relationship Analysis:**

This chart shows how {metric1.replace('_', ' ')} relates to {metric2.replace('_', ' ')}.

**What to look for:**
• If points form a line going up → When {metric1} increases, {metric2} also increases
• If points form a line going down → When {metric1} increases, {metric2} decreases  
• If points are scattered randomly → No clear relationship between them
"""
        
        elif chart_type == "box":
            fig = go.Figure()
            fig.add_trace(go.Box(y=self.df[metric1], name=metric1))
            fig.add_trace(go.Box(y=self.df[metric2], name=metric2))
            
            fig.update_layout(title=f"Comparing {metric1} and {metric2}")
            
            insight = f"""
**Distribution Comparison:**

This shows how values spread out for both metrics.

**Reading the boxes:**
• The line in middle = typical value (median)
• The box = where most values fall
• Dots above/below = unusual values
• Wider box = more variation
"""
        
        return fig, insight
    
    def create_category_breakdown(self, category_col, metric_col):
        """Break down a metric by category"""
        
        grouped = self.df.groupby(category_col)[metric_col].agg(['mean', 'sum', 'count'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=grouped.index,
            y=grouped['mean'],
            name='Average',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title=f"{metric_col.replace('_', ' ').title()} by {category_col.replace('_', ' ').title()}",
            xaxis_title=category_col.replace('_', ' ').title(),
            yaxis_title=f"Average {metric_col.replace('_', ' ').title()}"
        )
        
        best_category = grouped['mean'].idxmax()
        worst_category = grouped['mean'].idxmin()
        
        insight = f"""
**Performance by Category:**

**Best Performer:** {best_category} (Average: {grouped.loc[best_category, 'mean']:.2f})
**Needs Improvement:** {worst_category} (Average: {grouped.loc[worst_category, 'mean']:.2f})

**What this means:**
• Focus on what makes {best_category} successful
• Investigate why {worst_category} is underperforming
• Consider reallocating resources to top performers
"""
        
        return fig, insight
    
    def create_time_series_if_available(self, date_col, metric_col):
        """Create time series chart if date column exists"""
        
        try:
            df_temp = self.df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col])
            df_temp = df_temp.sort_values(date_col)
            
            fig = px.line(
                df_temp,
                x=date_col,
                y=metric_col,
                title=f"{metric_col.replace('_', ' ').title()} Over Time"
            )
            
            # Calculate trend
            first_half = df_temp[metric_col].iloc[:len(df_temp)//2].mean()
            second_half = df_temp[metric_col].iloc[len(df_temp)//2:].mean()
            
            if second_half > first_half * 1.1:
                trend = "📈 Growing"
                interpretation = "This metric is increasing over time - positive momentum!"
            elif second_half < first_half * 0.9:
                trend = "📉 Declining"
                interpretation = "⚠️ This metric is decreasing - investigate the cause"
            else:
                trend = "➡️ Stable"
                interpretation = "This metric is stable over time - consistent performance"
            
            insight = f"""
**Trend Over Time:**

**Current Trend:** {trend}

**Interpretation:** {interpretation}

**What to do:**
• Look for patterns (seasonality, cycles, sudden changes)
• Identify what caused major spikes or drops
• Use recent trends to forecast future performance
"""
            
            return fig, insight
            
        except Exception as e:
            return None, f"Could not create time series: {str(e)}"
    
    def generate_quick_insights(self, column):
        """Generate quick insights about any column"""
        
        col_type = self.column_types.get(column, "unknown")
        
        insights = []
        
        if col_type in ["integer", "float"]:
            data = self.df[column].dropna()
            
            insights.append(f"**Average:** {data.mean():.2f}")
            insights.append(f"**Typical Value (Median):** {data.median():.2f}")
            insights.append(f"**Range:** {data.min():.2f} to {data.max():.2f}")
            
            # Variability assessment
            cv = (data.std() / data.mean() * 100) if data.mean() != 0 else 0
            if cv < 10:
                insights.append("**Variability:** Very consistent (Low)")
            elif cv < 30:
                insights.append("**Variability:** Moderate")
            else:
                insights.append("**Variability:** ⚠️ Highly variable (Unpredictable)")
            
            # Missing data
            missing_pct = (self.df[column].isna().sum() / len(self.df)) * 100
            if missing_pct > 10:
                insights.append(f"⚠️ **Data Quality:** {missing_pct:.1f}% missing")
            else:
                insights.append("✅ **Data Quality:** Complete")
        
        elif col_type in ["categorical", "text", "boolean"]:
            value_counts = self.df[column].value_counts()
            
            insights.append(f"**Total Categories:** {self.df[column].nunique()}")
            insights.append(f"**Most Common:** {value_counts.index[0]} ({value_counts.iloc[0]} times)")
            
            concentration = (value_counts.iloc[0] / len(self.df)) * 100
            if concentration > 70:
                insights.append(f"⚠️ **Concentration Risk:** {concentration:.1f}% in one category")
            else:
                insights.append(f"✅ **Distribution:** Well balanced")
        
        return "\n".join(insights)
    
    def create_top_n_chart(self, column, n=10):
        """Create top N chart for any column"""
        
        value_counts = self.df[column].value_counts().head(n)
        
        fig = go.Figure(data=[
            go.Bar(
                x=value_counts.values,
                y=value_counts.index,
                orientation='h',
                marker_color='lightcoral',
                text=value_counts.values,
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=f"Top {n} in {column.replace('_', ' ').title()}",
            xaxis_title="Count",
            yaxis_title=column.replace('_', ' ').title(),
            height=400
        )
        
        total = value_counts.sum()
        top_pct = (value_counts.iloc[0] / total * 100) if len(value_counts) > 0 else 0
        
        insight = f"""
**Top Performers:**

• **#{1}:** {value_counts.index[0]} represents {top_pct:.1f}% of total
• Top {n} items account for {(value_counts.sum() / len(self.df) * 100):.1f}% of all records

**Business Implication:**
{"⚠️ High concentration in top item - diversification recommended" if top_pct > 40 else "✅ Good distribution across top items"}
"""
        
        return fig, insight