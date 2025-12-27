"""
Predictive Insights - Simple forecasting and "what-if" scenarios
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

class PredictiveInsights:
    """Generate simple predictions and forecasts"""
    
    def __init__(self, df, column_types):
        self.df = df
        self.column_types = column_types
        self.numeric_cols = [col for col, dtype in column_types.items() 
                            if dtype in ["integer", "float"]]
    
    def simple_forecast(self, column, periods=5):
        """Create simple linear forecast"""
        
        data = self.df[column].dropna()
        
        if len(data) < 10:
            return None, "Need at least 10 data points for forecasting"
        
        # Prepare data
        X = np.arange(len(data)).reshape(-1, 1)
        y = data.values
        
        # Fit model
        model = LinearRegression()
        model.fit(X, y)
        
        # Make predictions
        future_X = np.arange(len(data), len(data) + periods).reshape(-1, 1)
        predictions = model.predict(future_X)
        
        # Create chart
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=list(range(len(data))),
            y=data.values,
            mode='lines+markers',
            name='Historical',
            line=dict(color='blue')
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=list(range(len(data), len(data) + periods)),
            y=predictions,
            mode='lines+markers',
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=f"Forecast for {column.replace('_', ' ').title()}",
            xaxis_title="Time Period",
            yaxis_title=column.replace('_', ' ').title(),
            height=400
        )
        
        # Calculate trend
        trend = "increasing" if model.coef_[0] > 0 else "decreasing"
        avg_change = model.coef_[0]
        
        current_avg = data.mean()
        forecast_avg = predictions.mean()
        change_pct = ((forecast_avg - current_avg) / current_avg * 100) if current_avg != 0 else 0
        
        insight = f"""
**Forecast Summary:**

**Current Average:** {current_avg:.2f}
**Predicted Average (next {periods} periods):** {forecast_avg:.2f}
**Expected Change:** {change_pct:+.1f}%

**Trend Direction:** {"📈 Growing" if trend == "increasing" else "📉 Declining"}
**Rate of Change:** {abs(avg_change):.2f} per period

**What This Means:**
"""
        
        if trend == "increasing":
            insight += f"• This metric is expected to grow by {abs(change_pct):.1f}% in the near future\n"
            insight += "• ✅ Positive momentum - consider investing more resources\n"
            insight += "• Plan capacity and resources for continued growth"
        else:
            insight += f"• ⚠️ This metric is expected to decline by {abs(change_pct):.1f}%\n"
            insight += "• Investigate root causes immediately\n"
            insight += "• Develop action plan to reverse the trend"
        
        return fig, insight
    
    def what_if_analysis(self, metric_col, impact_col, scenario_change_pct):
        """Simple what-if scenario analysis"""
        
        # Calculate correlation
        corr = self.df[[metric_col, impact_col]].corr().iloc[0, 1]
        
        if abs(corr) < 0.3:
            return None, f"Weak relationship between {metric_col} and {impact_col} - scenario analysis not meaningful"
        
        # Current averages
        current_metric = self.df[metric_col].mean()
        current_impact = self.df[impact_col].mean()
        
        # Scenario calculation
        new_metric = current_metric * (1 + scenario_change_pct / 100)
        # Simple proportional impact based on correlation
        estimated_impact = current_impact * (1 + (scenario_change_pct / 100) * corr)
        impact_change = estimated_impact - current_impact
        impact_change_pct = (impact_change / current_impact * 100) if current_impact != 0 else 0
        
        # Create visualization
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[metric_col, impact_col],
            y=[current_metric, current_impact],
            name='Current',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            x=[metric_col, impact_col],
            y=[new_metric, estimated_impact],
            name='Scenario',
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            title=f"What-If: {scenario_change_pct:+.0f}% Change in {metric_col.replace('_', ' ').title()}",
            yaxis_title="Value",
            barmode='group',
            height=400
        )
        
        insight = f"""
**Scenario Analysis:**

**If {metric_col.replace('_', ' ')} changes by {scenario_change_pct:+.1f}%:**

📊 **Direct Impact:**
• {metric_col.replace('_', ' ').title()}: {current_metric:.2f} → {new_metric:.2f}

📈 **Estimated Ripple Effect:**
• {impact_col.replace('_', ' ').title()}: {current_impact:.2f} → {estimated_impact:.2f}
• Expected change: {impact_change_pct:+.1f}%

**Relationship Strength:** {"Strong" if abs(corr) > 0.7 else "Moderate"} (correlation: {corr:.2f})

**Business Implication:**
"""
        
        if scenario_change_pct > 0:
            insight += f"• Increasing {metric_col} by {scenario_change_pct}% could boost {impact_col} by {abs(impact_change_pct):.1f}%\n"
            insight += "• Consider this when planning growth initiatives"
        else:
            insight += f"• ⚠️ Reducing {metric_col} by {abs(scenario_change_pct)}% might decrease {impact_col} by {abs(impact_change_pct):.1f}%\n"
            insight += "• Evaluate if cost savings justify the impact"
        
        return fig, insight
    
    def identify_key_drivers(self, target_metric):
        """Identify which factors most influence a target metric"""
        
        if target_metric not in self.numeric_cols:
            return None, "Target must be a numeric column"
        
        # Calculate correlations with target
        correlations = {}
        for col in self.numeric_cols:
            if col != target_metric:
                corr = self.df[[target_metric, col]].corr().iloc[0, 1]
                if not np.isnan(corr):
                    correlations[col] = abs(corr)
        
        # Sort by importance
        sorted_drivers = sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:5]
        
        if not sorted_drivers:
            return None, "No significant drivers found"
        
        # Create chart
        fig = go.Figure(data=[
            go.Bar(
                x=[driver[0].replace('_', ' ').title() for driver in sorted_drivers],
                y=[driver[1] for driver in sorted_drivers],
                marker_color=['darkgreen' if v > 0.7 else 'orange' if v > 0.4 else 'lightblue' 
                             for _, v in sorted_drivers],
                text=[f"{v:.2f}" for _, v in sorted_drivers],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=f"Key Drivers of {target_metric.replace('_', ' ').title()}",
            xaxis_title="Factors",
            yaxis_title="Influence Strength",
            height=400
        )
        
        top_driver = sorted_drivers[0]
        
        insight = f"""
**Key Performance Drivers:**

**Most Important Factor:** {top_driver[0].replace('_', ' ').title()} (Influence: {top_driver[1]:.0%})

**Top 5 Drivers:**
"""
        
        for i, (driver, strength) in enumerate(sorted_drivers, 1):
            impact = "🔴 Critical" if strength > 0.7 else "🟡 Important" if strength > 0.4 else "🔵 Moderate"
            insight += f"{i}. {driver.replace('_', ' ').title()} - {impact} ({strength:.0%})\n"
        
        insight += f"""

**Strategic Recommendations:**
• Focus improvement efforts on {top_driver[0].replace('_', ' ')} - it has the biggest impact
• Monitor these top 5 factors closely as they drive {target_metric.replace('_', ' ')}
• Small improvements in key drivers can create significant results
"""
        
        return fig, insight
    
    def calculate_roi_projection(self, investment_col, return_col, investment_amount):
        """Calculate ROI projection based on historical data"""
        
        # Filter out zero investments
        mask = (self.df[investment_col] > 0) & (self.df[return_col] > 0)
        filtered_df = self.df[mask]
        
        if len(filtered_df) < 5:
            return None, "Not enough data for ROI calculation"
        
        # Calculate historical ROI
        filtered_df['roi'] = (filtered_df[return_col] / filtered_df[investment_col]) * 100
        avg_roi = filtered_df['roi'].mean()
        
        # Project returns
        projected_return = investment_amount * (avg_roi / 100)
        
        insight = f"""
**ROI Projection:**

**Investment Amount:** ${investment_amount:,.2f}
**Historical Average ROI:** {avg_roi:.1f}%
**Projected Return:** ${projected_return:,.2f}
**Net Gain:** ${projected_return - investment_amount:,.2f}

**Confidence Level:**
"""
        
        roi_std = filtered_df['roi'].std()
        if roi_std < 10:
            insight += "🟢 High (Consistent historical returns)\n"
        elif roi_std < 30:
            insight += "🟡 Medium (Moderate variability)\n"
        else:
            insight += "🔴 Low (High variability - results may vary significantly)\n"
        
        insight += f"""

**Best Case:** ${investment_amount * ((avg_roi + roi_std) / 100):,.2f} return
**Worst Case:** ${investment_amount * ((avg_roi - roi_std) / 100):,.2f} return

**Recommendation:**
"""
        
        if avg_roi > 20:
            insight += "✅ Strong ROI potential - favorable investment opportunity"
        elif avg_roi > 10:
            insight += "⚠️ Moderate ROI - evaluate against other opportunities"
        else:
            insight += "❌ Low ROI - consider alternative investments"
        
        return None, insight