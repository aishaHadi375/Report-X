"""
AI-Powered Natural Language Report Generator
Uses Claude API to create human-readable business reports
"""

import json
from datetime import datetime

class AIReportGenerator:
    """Generate natural language reports using Claude API"""
    
    def __init__(self, trend_analyzer, anomaly_detector, insight_generator):
        self.trend_analyzer = trend_analyzer
        self.anomaly_detector = anomaly_detector
        self.insight_generator = insight_generator
    
    async def generate_executive_report(self):
        """Generate a complete executive report in natural language"""
        
        # Gather all analysis data
        trends = self.trend_analyzer.analyze_trends()
        anomalies = self.anomaly_detector.detect_all_anomalies()
        summary = self.insight_generator.generate_executive_summary()
        actions = self.insight_generator.generate_business_actions()
        
        # Create structured prompt for Claude
        prompt = self._build_report_prompt(trends, anomalies, summary, actions)
        
        try:
            # Call Claude API
            response = await fetch("https://api.anthropic.com/v1/messages", {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": json.dumps({
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 4000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                })
            })
            
            data = await response.json()
            report_text = data['content'][0]['text']
            
            return {
                "success": True,
                "report": report_text,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_report": self._generate_fallback_report(summary, actions)
            }
    
    def _build_report_prompt(self, trends, anomalies, summary, actions):
        """Build a comprehensive prompt for Claude"""
        
        prompt = f"""You are a senior business analyst writing an executive report for a non-technical business leader. 

Your task is to analyze this data and create a clear, compelling, action-oriented report that a CEO or business owner can read in 5 minutes and immediately understand what's happening in their business.

DATA ANALYSIS RESULTS:
======================

DATASET OVERVIEW:
- Size: {summary['dataset_size']}
- Data Quality Score: {summary['data_quality']['score']}% ({summary['data_quality']['grade']})
- Quality Assessment: {summary['data_quality']['recommendation']}

KEY METRICS PERFORMANCE:
{json.dumps(summary['key_metrics'], indent=2)}

ALERTS & ISSUES:
{json.dumps(summary['alerts'], indent=2)}

DETECTED ANOMALIES:
- Outliers: {json.dumps(anomalies['outliers'], indent=2)}
- Missing Data: {anomalies['missing_patterns']['total_missing_cells']} cells missing
- Duplicates: {anomalies['duplicates']['count']} duplicate records
- Data Quality Issues: {json.dumps(anomalies['data_quality_issues'], indent=2)}

NUMERIC TRENDS:
{json.dumps(trends['numeric_trends'], indent=2)}

CATEGORICAL DISTRIBUTIONS:
{json.dumps(trends['categorical_distributions'], indent=2)}

TOP PRIORITY ACTIONS:
{json.dumps(actions[:5], indent=2)}

WRITE A COMPREHENSIVE EXECUTIVE REPORT WITH THESE SECTIONS:

1. **EXECUTIVE SUMMARY** (2-3 paragraphs)
   - Start with the single most important finding
   - Overall health of the business based on data
   - Immediate actions needed

2. **WHAT YOUR DATA TELLS US** (4-5 key insights)
   - Translate numbers into business stories
   - Use analogies and plain language
   - Focus on "what this means for your business"

3. **RED FLAGS & URGENT ISSUES** (if any)
   - Critical problems requiring immediate attention
   - Potential revenue/cost impacts
   - Quick fixes vs long-term solutions

4. **OPPORTUNITIES FOR GROWTH**
   - Positive trends to capitalize on
   - Untapped potential in the data
   - Strategic recommendations

5. **YOUR 30-DAY ACTION PLAN**
   - Week 1: Critical fixes
   - Week 2-3: High priority improvements
   - Week 4: Strategic initiatives
   - Expected outcomes and benefits

6. **DATA QUALITY REPORT CARD**
   - What's working well
   - What needs improvement
   - Impact on decision-making reliability

WRITING STYLE REQUIREMENTS:
- Write in first person ("I analyzed your data...")
- Use conversational, confident tone
- NO jargon - explain everything in simple terms
- Use analogies and real-world examples
- Be direct and honest about problems
- Focus on actionable insights, not just observations
- Include specific numbers and percentages to build credibility
- End each section with clear "what to do next" guidance

Make it feel like a trusted advisor is explaining the business to the owner over coffee, not a technical report.

Begin the report now:"""

        return prompt
    
    def _generate_fallback_report(self, summary, actions):
        """Generate a basic report if API fails"""
        
        report = f"""
# EXECUTIVE BUSINESS REPORT
Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

## 📊 AT A GLANCE

Your dataset contains **{summary['dataset_size']}** with an overall data quality score of **{summary['data_quality']['score']}%**.

**Quality Grade:** {summary['data_quality']['grade']}
**Assessment:** {summary['data_quality']['recommendation']}

## 🎯 KEY METRICS SNAPSHOT

"""
        for metric in summary['key_metrics'][:3]:
            report += f"**{metric['name']}:** {metric['trend']} (Average: {metric['average']})\n"
        
        report += "\n## 🚨 URGENT ATTENTION REQUIRED\n\n"
        
        if summary['alerts']:
            for alert in summary['alerts']:
                report += f"- {alert}\n"
        else:
            report += "✅ No urgent issues detected\n"
        
        report += "\n## 💡 TOP 3 PRIORITY ACTIONS\n\n"
        
        for i, action in enumerate(actions[:3], 1):
            report += f"""
### {i}. {action['Action']}

**Why this matters:** {action['Reason']}

**What to do now:** {action['Quick Win']}

**Expected benefit:** {action['Expected Benefit']}

**Owner:** {action['Owner']} | **Timeline:** {action['Timeline']}

---
"""
        
        report += """
## 📈 NEXT STEPS

1. Review the priority actions above with your team
2. Assign owners and set deadlines for each action
3. Schedule a follow-up review in 2 weeks
4. Use the detailed analysis sections for deeper insights

---

*This is an automated analysis. For best results, review with your data team.*
"""
        
        return report
    
    def generate_one_page_summary(self, summary, actions):
        """Generate a one-page summary for quick reference"""
        
        critical_actions = [a for a in actions if "🔴" in a['Priority']]
        high_actions = [a for a in actions if "🟡" in a['Priority']]
        
        one_pager = f"""
# ONE-PAGE BUSINESS SUMMARY
{datetime.now().strftime("%B %d, %Y")}

## THE HEADLINE
{summary['data_quality']['recommendation']}

## BY THE NUMBERS
- **Data Quality:** {summary['data_quality']['score']}% {summary['data_quality']['grade']}
- **Records Analyzed:** {summary['dataset_size']}
- **Critical Issues:** {len(critical_actions)}
- **Quick Wins Available:** {len(high_actions)}

## TOP 3 THINGS YOU NEED TO KNOW

"""
        for i, metric in enumerate(summary['key_metrics'][:3], 1):
            one_pager += f"{i}. **{metric['name']}** is {metric['trend'].lower()} (avg: {metric['average']})\n"
        
        one_pager += f"""

## THIS WEEK'S PRIORITIES

"""
        for i, action in enumerate(actions[:3], 1):
            one_pager += f"**{i}.** {action['Action']} → {action['Owner']}\n"
        
        one_pager += f"""

## BOTTOM LINE
{"✅ Your data is in good shape. Focus on growth opportunities." if summary['data_quality']['score'] > 85 else "⚠️ Data quality needs attention before making major decisions."}

---
*Full detailed report available in the complete analysis*
"""
        
        return one_pager
    
    def export_to_pdf_format(self, report_text):
        """Format report for PDF export (returns markdown with styling)"""
        
        styled_report = f"""
<style>
@page {{
    margin: 2cm;
}}
body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}}
h1 {{
    color: #1f77b4;
    border-bottom: 3px solid #1f77b4;
    padding-bottom: 10px;
}}
h2 {{
    color: #2ca02c;
    margin-top: 30px;
}}
.highlight {{
    background: #fff3cd;
    padding: 15px;
    border-left: 4px solid #ffc107;
    margin: 20px 0;
}}
.critical {{
    background: #f8d7da;
    padding: 15px;
    border-left: 4px solid #dc3545;
    margin: 20px 0;
}}
.success {{
    background: #d4edda;
    padding: 15px;
    border-left: 4px solid #28a745;
    margin: 20px 0;
}}
</style>

{report_text}

---

**Report Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
**Analysis Tool:** AI Workflow & Report Generator
"""
        
        return styled_report