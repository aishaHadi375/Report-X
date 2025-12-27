import pandas as pd

class BusinessInsightGenerator:
    """Generate actionable business insights from data analysis"""
    
    def __init__(self, trend_analyzer):
        self.trend_analyzer = trend_analyzer
    
    def generate_business_actions(self):
        """Generate comprehensive business-focused insights with priorities"""
        actions = []
        df = self.trend_analyzer.df
        total_rows = len(df)
        
        # 1. Critical: Missing Data Actions
        missing_pct = (df.isnull().sum() / total_rows) * 100
        for col, pct in missing_pct.items():
            if pct > 30:
                actions.append({
                    "Category": "🚨 Data Quality Crisis",
                    "Action": f"Urgently fix data collection for '{col.replace('_', ' ').title()}'",
                    "Reason": f"{pct:.1f}% missing means nearly 1 in 3 records lack this information",
                    "Impact": "Critical - Your reports and decisions based on this field are unreliable",
                    "Quick Win": f"Make '{col}' a mandatory field in your data entry system TODAY",
                    "Long Term": "Train staff on importance of complete data entry",
                    "Expected Benefit": "Reliable analysis and confident decision-making",
                    "Priority": "🔴 Critical Priority",
                    "Owner": "Data Team / Operations Lead",
                    "Timeline": "Fix within 1 week"
                })
            elif pct > 10:
                actions.append({
                    "Category": "⚠️ Data Quality Issue",
                    "Action": f"Improve completeness of '{col.replace('_', ' ').title()}' field",
                    "Reason": f"{pct:.1f}% missing suggests inconsistent data capture",
                    "Impact": "Medium - Gaps in data limit analysis accuracy",
                    "Quick Win": "Add validation rules and helpful prompts at data entry",
                    "Long Term": "Review and update data collection procedures",
                    "Expected Benefit": "More complete data for better insights",
                    "Priority": "🟡 High Priority",
                    "Owner": "Operations Manager",
                    "Timeline": "Fix within 2-4 weeks"
                })
        
        # 2. High Risk: Variability Warnings
        numeric_trends = self.trend_analyzer._analyze_numeric_trends()
        for col, info in numeric_trends.items():
            cv = info.get("coefficient_of_variation", 0)
            if cv > 100:
                actions.append({
                    "Category": "⚠️ High Risk Alert",
                    "Action": f"Investigate extreme swings in '{col.replace('_', ' ').title()}'",
                    "Reason": f"Values fluctuate wildly (variation of {cv:.0f}%) - either data errors or business volatility",
                    "Impact": "High - Unpredictable metrics make planning impossible",
                    "Quick Win": "Review top and bottom 10 values for obvious data entry errors",
                    "Long Term": "Implement data validation rules to prevent outlier entries",
                    "Expected Benefit": "Stable, trustworthy metrics for forecasting",
                    "Priority": "🔴 Critical Priority",
                    "Owner": "Data Quality Team / Finance",
                    "Timeline": "Investigate within 3 days"
                })
        
        # 3. Urgent: Declining Business Metrics
        for col, info in numeric_trends.items():
            if info["trend_direction"] == "decreasing":
                avg_decline = ((info['mean'] - info['median']) / info['mean'] * 100) if info['mean'] != 0 else 0
                actions.append({
                    "Category": "📉 Performance Alert",
                    "Action": f"Address declining performance in '{col.replace('_', ' ').title()}'",
                    "Reason": f"Recent values significantly lower than historical average",
                    "Impact": "Critical - Declining trend indicates potential business problem",
                    "Quick Win": "Hold emergency meeting with team to identify root cause",
                    "Long Term": "Develop action plan to reverse the decline",
                    "Expected Benefit": "Stop revenue/performance loss, return to growth",
                    "Priority": "🔴 Critical Priority",
                    "Owner": "Department Head / Management",
                    "Timeline": "Meet within 48 hours"
                })
        
        # 4. Opportunity: Growth Trends
        for col, info in numeric_trends.items():
            if info["trend_direction"] == "increasing":
                actions.append({
                    "Category": "📈 Growth Opportunity",
                    "Action": f"Double down on success in '{col.replace('_', ' ').title()}'",
                    "Reason": f"Strong upward trend shows what's working well",
                    "Impact": "High Potential - Opportunity to accelerate growth",
                    "Quick Win": "Analyze what's driving growth and document best practices",
                    "Long Term": "Allocate more resources to replicate success in other areas",
                    "Expected Benefit": "Accelerated growth and competitive advantage",
                    "Priority": "🟢 Strategic Opportunity",
                    "Owner": "Strategy Team / Business Development",
                    "Timeline": "Capitalize within 1 month"
                })
        
        # 5. Planning: Stable Metrics for Forecasting
        for col, info in numeric_trends.items():
            if info["trend_direction"] == "stable" and info.get("coefficient_of_variation", 0) < 10:
                actions.append({
                    "Category": "📊 Planning Asset",
                    "Action": f"Use '{col.replace('_', ' ').title()}' as forecasting baseline",
                    "Reason": f"Highly stable and predictable values (variation < 10%)",
                    "Impact": "Medium - Improves planning accuracy",
                    "Quick Win": "Build next quarter's forecast using this reliable metric",
                    "Long Term": "Develop KPI dashboard featuring stable metrics",
                    "Expected Benefit": "More accurate forecasts and budgets",
                    "Priority": "🟢 Strategic Opportunity",
                    "Owner": "Planning / Finance Team",
                    "Timeline": "Implement within 2 weeks"
                })
        
        # 6. Risk Management: Concentration Issues
        cat_distributions = self.trend_analyzer._analyze_categorical_distributions()
        for col, info in cat_distributions.items():
            concentration = info.get("concentration", 0)
            if concentration > 70:
                actions.append({
                    "Category": "⚠️ Concentration Risk",
                    "Action": f"Diversify beyond '{info['most_common']}' in {col.replace('_', ' ').title()}",
                    "Reason": f"Over-reliance on one category ({concentration:.1f}% concentration) creates vulnerability",
                    "Impact": "High Risk - Single point of failure could devastate business",
                    "Quick Win": "Identify 2-3 alternative categories to develop immediately",
                    "Long Term": "Set target: No single category should exceed 40% within 6 months",
                    "Expected Benefit": "Reduced risk, more stable revenue streams",
                    "Priority": "🟡 High Priority",
                    "Owner": "Business Development / Sales",
                    "Timeline": "Start diversification within 2 weeks"
                })
            elif concentration < 20:
                actions.append({
                    "Category": "✅ Balanced Portfolio",
                    "Action": f"Maintain diversity in '{col.replace('_', ' ').title()}'",
                    "Reason": f"Excellent balance across categories (top category only {concentration:.1f}%)",
                    "Impact": "Positive - Reduced risk from diversification",
                    "Quick Win": "Document what enabled this balance as best practice",
                    "Long Term": "Use this as model for other business areas",
                    "Expected Benefit": "Continued stable, resilient performance",
                    "Priority": "🟢 Strategic Opportunity",
                    "Owner": "Strategy Team",
                    "Timeline": "Document within 1 week"
                })
        
        # 7. Strategic: Leverage Correlations
        correlations = self.trend_analyzer._analyze_correlations()
        for pair, info in correlations.items():
            if info['strength'] == 'strong positive':
                actions.append({
                    "Category": "🔗 Strategic Insight",
                    "Action": f"Leverage relationship between {pair}",
                    "Reason": f"Strong correlation ({info['coefficient']:.2f}) means they move together predictably",
                    "Impact": "Medium - Can use one to predict the other",
                    "Quick Win": "Use leading indicator to forecast lagging metric",
                    "Long Term": "Build predictive model using this relationship",
                    "Expected Benefit": "Earlier warnings and better forecasting",
                    "Priority": "🟢 Strategic Opportunity",
                    "Owner": "Analytics / Data Science Team",
                    "Timeline": "Build model within 3-4 weeks"
                })
        
        # 8. Foundation: Overall Data Quality Initiative
        total_cells = total_rows * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        quality_score = ((total_cells - missing_cells) / total_cells) * 100
        quality_score -= (duplicate_rows / total_rows) * 10
        
        if quality_score < 80:
            actions.append({
                "Category": "🚨 Data Governance Crisis",
                "Action": "Launch comprehensive data quality improvement program",
                "Reason": f"Overall data quality score is {quality_score:.1f}% (minimum acceptable: 80%)",
                "Impact": "Critical - Poor quality undermines ALL business decisions",
                "Quick Win": "Appoint Data Quality Champion and form improvement team",
                "Long Term": "Implement data governance framework with monthly quality reviews",
                "Expected Benefit": "Trustworthy data foundation for all business decisions",
                "Priority": "🔴 Critical Priority",
                "Owner": "Chief Data Officer / Senior Leadership",
                "Timeline": "Kickoff within 1 week"
            })
        elif quality_score >= 90:
            actions.append({
                "Category": "✅ Data Excellence",
                "Action": "Maintain and showcase data quality standards",
                "Reason": f"Outstanding data quality score of {quality_score:.1f}%",
                "Impact": "High Positive - Enables confident decision-making",
                "Quick Win": "Document data quality practices for other teams",
                "Long Term": "Establish your team as center of excellence",
                "Expected Benefit": "Continued high-quality insights and decisions",
                "Priority": "🟢 Strategic Opportunity",
                "Owner": "Data Team Lead",
                "Timeline": "Document within 2 weeks"
            })
        
        # Sort by priority (Critical → High → Strategic)
        priority_order = {
            "🔴 Critical Priority": 0, 
            "🟡 High Priority": 1, 
            "🟢 Strategic Opportunity": 2
        }
        actions.sort(key=lambda x: priority_order.get(x["Priority"], 3))
        
        return actions
    
    def generate_executive_summary(self):
        """Generate executive summary with clear business language"""
        df = self.trend_analyzer.df
        numeric_trends = self.trend_analyzer._analyze_numeric_trends()
        cat_distributions = self.trend_analyzer._analyze_categorical_distributions()
        
        summary = {
            "dataset_size": f"{len(df):,} records covering {len(df.columns)} different measurements",
            "data_quality": self._calculate_quality_score(df),
            "key_metrics": self._identify_key_metrics(numeric_trends),
            "alerts": self._identify_alerts(numeric_trends, df),
            "opportunities": self._identify_opportunities(numeric_trends, cat_distributions)
        }
        
        return summary
    
    def _calculate_quality_score(self, df):
        """Calculate overall data quality score with grades"""
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        uniqueness = ((len(df) - duplicate_rows) / len(df)) * 100
        
        overall_score = (completeness * 0.6 + uniqueness * 0.4)
        
        if overall_score >= 95:
            grade = "Excellent ⭐⭐⭐⭐⭐"
            recommendation = "Your data is pristine! Continue current practices."
        elif overall_score >= 85:
            grade = "Very Good ⭐⭐⭐⭐"
            recommendation = "Minor improvements needed, but generally reliable."
        elif overall_score >= 75:
            grade = "Good ⭐⭐⭐"
            recommendation = "Some cleanup needed for optimal analysis."
        elif overall_score >= 60:
            grade = "Fair ⭐⭐"
            recommendation = "Significant quality issues - prioritize data cleanup."
        else:
            grade = "Poor ⭐"
            recommendation = "⚠️ Critical quality issues - data needs major cleanup before use."
        
        return {
            "score": round(overall_score, 1),
            "grade": grade,
            "completeness": round(completeness, 1),
            "uniqueness": round(uniqueness, 1),
            "recommendation": recommendation
        }
    
    def _identify_key_metrics(self, numeric_trends):
        """Identify most important metrics with business context"""
        key_metrics = []
        
        for col, info in list(numeric_trends.items())[:3]:
            variability = "High" if info.get('coefficient_of_variation', 0) > 50 else "Low"
            trend_symbol = "📈" if info['trend_direction'] == 'increasing' else "📉" if info['trend_direction'] == 'decreasing' else "➡️"
            
            key_metrics.append({
                "name": col.replace('_', ' ').title(),
                "average": round(info['mean'], 2),
                "trend": f"{trend_symbol} {info['trend_direction'].title()}",
                "variability": variability,
                "range": f"{info['min']:.1f} to {info['max']:.1f}"
            })
        
        return key_metrics
    
    def _identify_alerts(self, numeric_trends, df):
        """Identify urgent issues requiring immediate attention"""
        alerts = []
        
        # Check for declining trends
        declining_count = sum(1 for info in numeric_trends.values() if info['trend_direction'] == 'decreasing')
        if declining_count > 0:
            alerts.append(f"🚨 {declining_count} metric(s) showing decline - requires immediate investigation")
        
        # Check for high variability
        volatile_count = sum(1 for info in numeric_trends.values() if info.get('coefficient_of_variation', 0) > 100)
        if volatile_count > 0:
            alerts.append(f"⚠️ {volatile_count} metric(s) highly volatile - check for data quality issues")
        
        # Check for excessive missing data
        high_missing = sum(1 for col in df.columns if df[col].isnull().sum() / len(df) > 0.3)
        if high_missing > 0:
            alerts.append(f"⚠️ {high_missing} field(s) missing >30% of data - impacts analysis reliability")
        
        # Check for duplicates
        dup_pct = (df.duplicated().sum() / len(df)) * 100
        if dup_pct > 5:
            alerts.append(f"⚠️ {dup_pct:.1f}% duplicate records detected - may inflate results")
        
        return alerts if alerts else ["✅ No urgent issues detected - data looks healthy"]
    
    def _identify_opportunities(self, numeric_trends, cat_distributions):
        """Identify growth opportunities and positive trends"""
        opportunities = []
        
        # Check for growing metrics
        growing_count = sum(1 for info in numeric_trends.values() if info['trend_direction'] == 'increasing')
        if growing_count > 0:
            opportunities.append(f"📈 {growing_count} metric(s) growing - identify and replicate success factors")
        
        # Check for stable predictable metrics
        stable_count = sum(1 for info in numeric_trends.values() 
                          if info['trend_direction'] == 'stable' and info.get('coefficient_of_variation', 0) < 10)
        if stable_count > 0:
            opportunities.append(f"📊 {stable_count} stable metric(s) - excellent for reliable forecasting")
        
        # Check for balanced distributions
        balanced_count = sum(1 for info in cat_distributions.values() if info.get('concentration', 100) < 30)
        if balanced_count > 0:
            opportunities.append(f"✅ {balanced_count} well-diversified category - reduced concentration risk")
        
        return opportunities if opportunities else ["Continue monitoring current performance trends"]
    
    def generate_top_3_insights(self):
        """Generate the top 3 most important business insights"""
        actions = self.generate_business_actions()
        
        # Get top 3 critical/high priority items
        top_actions = [a for a in actions if a['Priority'] in ['🔴 Critical Priority', '🟡 High Priority']][:3]
        
        if len(top_actions) < 3:
            # Add strategic opportunities if needed
            strategic = [a for a in actions if a['Priority'] == '🟢 Strategic Opportunity']
            top_actions.extend(strategic[:3-len(top_actions)])
        
        return top_actions