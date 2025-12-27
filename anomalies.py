import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AnomalyDetector:
    """Detects and visualizes anomalies in data with business-friendly explanations"""
    
    def __init__(self, df, column_types):
        self.df = df
        self.column_types = column_types
        self.numeric_cols = [col for col, dtype in column_types.items() 
                            if dtype in ["integer", "float"]]
        self.categorical_cols = [col for col, dtype in column_types.items() 
                                if dtype in ["categorical", "boolean", "text"]]
    
    def detect_all_anomalies(self):
        """Detect all types of anomalies"""
        anomalies = {
            'outliers': self._detect_outliers(),
            'missing_patterns': self._detect_missing_patterns(),
            'duplicates': self._detect_duplicates(),
            'unusual_distributions': self._detect_unusual_distributions(),
            'data_quality_issues': self._detect_data_quality_issues()
        }
        return anomalies
    
    def _detect_outliers(self):
        """Detect statistical outliers using IQR method"""
        outliers = {}
        
        for col in self.numeric_cols[:5]:  # Limit to first 5 numeric columns
            data = self.df[col].dropna()
            if len(data) == 0:
                continue
                
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (data < lower_bound) | (data > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                outliers[col] = {
                    'count': int(outlier_count),
                    'percentage': float((outlier_count / len(data)) * 100),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'min_outlier': float(data[outlier_mask].min()),
                    'max_outlier': float(data[outlier_mask].max())
                }
        
        return outliers
    
    def _detect_missing_patterns(self):
        """Identify patterns in missing data"""
        missing_info = {}
        
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                missing_info[col] = {
                    'count': int(missing_count),
                    'percentage': float((missing_count / len(self.df)) * 100)
                }
        
        # Rows with multiple missing values
        rows_with_missing = (self.df.isnull().sum(axis=1) > len(self.df.columns) * 0.3).sum()
        
        return {
            'by_column': missing_info,
            'problematic_rows': int(rows_with_missing),
            'total_missing_cells': int(self.df.isnull().sum().sum())
        }
    
    def _detect_duplicates(self):
        """Detect duplicate rows"""
        duplicate_count = self.df.duplicated().sum()
        return {
            'count': int(duplicate_count),
            'percentage': float((duplicate_count / len(self.df)) * 100)
        }
    
    def _detect_unusual_distributions(self):
        """Detect unusual value distributions"""
        unusual = {}
        
        for col in self.numeric_cols[:5]:
            data = self.df[col].dropna()
            if len(data) == 0:
                continue
            
            # Check for high concentration of zeros
            zero_pct = (data == 0).sum() / len(data) * 100
            if zero_pct > 30:
                unusual[col] = unusual.get(col, {})
                unusual[col]['excessive_zeros'] = float(zero_pct)
            
            # Check for negative values in typically positive columns
            if any(keyword in col.lower() for keyword in ['price', 'amount', 'quantity', 'age', 'count']):
                negative_count = (data < 0).sum()
                if negative_count > 0:
                    unusual[col] = unusual.get(col, {})
                    unusual[col]['unexpected_negatives'] = int(negative_count)
        
        return unusual
    
    def _detect_data_quality_issues(self):
        """Identify data quality problems"""
        issues = {}
        
        # Constant columns (all same value)
        constant_cols = [col for col in self.df.columns if self.df[col].nunique() == 1]
        if constant_cols:
            issues['constant_columns'] = constant_cols
        
        # High cardinality categorical columns
        high_cardinality = []
        for col in self.categorical_cols:
            if self.df[col].nunique() > len(self.df) * 0.8:
                high_cardinality.append(col)
        if high_cardinality:
            issues['high_cardinality'] = high_cardinality
        
        # Mostly missing columns
        mostly_missing = [col for col in self.df.columns 
                         if self.df[col].isnull().sum() > len(self.df) * 0.7]
        if mostly_missing:
            issues['mostly_missing'] = mostly_missing
        
        return issues
    
    def visualize_outliers(self, top_n=3):
     """Create line plots showing numeric trends with outliers highlighted"""
     outlier_info = self._detect_outliers()
    
     if not outlier_info:
        return None, "✅ **Great News!** No unusual values detected in your data. All numbers fall within expected ranges."
    
    # Select top N columns with most outliers
     sorted_cols = sorted(outlier_info.items(), 
                       key=lambda x: x[1]['count'], 
                       reverse=True)[:top_n]
    
     fig = make_subplots(
        rows=1, cols=len(sorted_cols),
        subplot_titles=[col.replace('_', ' ').title() for col, _ in sorted_cols]
    )
    
     for idx, (col, info) in enumerate(sorted_cols, 1):
        data = self.df[col].dropna()
        indices = data.index
        
        # Create a line for the main data
        fig.add_trace(
            go.Scatter(
                x=indices,
                y=data,
                mode='lines+markers',
                name=col,
                line=dict(color='blue'),
                marker=dict(size=6, color='blue')
            ),
            row=1, col=idx
        )
        
        # Highlight outliers in red
        outlier_mask = (data < info['lower_bound']) | (data > info['upper_bound'])
        if outlier_mask.any():
            fig.add_trace(
                go.Scatter(
                    x=indices[outlier_mask],
                    y=data[outlier_mask],
                    mode='markers',
                    name='Outliers',
                    marker=dict(color='red', size=8, symbol='x')
                ),
                row=1, col=idx
            )
    
     fig.update_layout(
        title="Numeric Trends with Outliers Highlighted",
        showlegend=False,
        height=400
    )
    
    # Generate business-friendly insight
     total_outliers = sum(info['count'] for _, info in sorted_cols)
     worst_col, worst_info = sorted_cols[0]
    
     insight = f"""📊 **What This Chart Shows:**
    
This line chart displays the trend of numeric values across your records. Red markers indicate unusual values (outliers) that deviate from expected ranges.

🎯 **Key Findings:**
• Found **{total_outliers} unusual values** across {len(sorted_cols)} different metrics
• **'{worst_col.replace('_', ' ').title()}'** has the most unusual values ({worst_info['count']} records)

💡 **What This Means for Your Business:**
• Outliers could be data entry errors or special exceptional cases
• Investigate these points to ensure data accuracy

🔍 **Normal Range for '{worst_col.replace('_', ' ').title()}':**
Expected values should be between {worst_info['lower_bound']:.2f} and {worst_info['upper_bound']:.2f}
"""
    
     return fig, insight

    
    def visualize_missing_data(self):
        """Create visualization of missing data patterns"""
        missing_info = self._detect_missing_patterns()
        
        if not missing_info['by_column']:
            return None, "✅ **Excellent!** Your data is complete with no missing information."
        
        # Create bar chart for missing data by column
        missing_df = pd.DataFrame(missing_info['by_column']).T
        missing_df = missing_df.sort_values('percentage', ascending=False)
        
        fig = go.Figure(data=[
            go.Bar(
                x=missing_df.index,
                y=missing_df['percentage'],
                text=missing_df['count'],
                texttemplate='%{text} missing',
                textposition='outside',
                marker_color=['red' if x > 50 else 'orange' if x > 20 else 'yellow' 
                             for x in missing_df['percentage']]
            )
        ])
        
        fig.update_layout(
            title="Missing Information by Field",
            xaxis_title="Field Name",
            yaxis_title="Percentage Missing (%)",
            height=400
        )
        
        # Generate insight
        total_missing_pct = (missing_info['total_missing_cells'] / 
                            (len(self.df) * len(self.df.columns))) * 100
        worst_col = max(missing_info['by_column'].items(), 
                       key=lambda x: x[1]['percentage'])
        
        insight = f"""📊 **What This Chart Shows:**

This chart reveals which information fields are incomplete in your data. Higher bars mean more missing information.

🎯 **Key Findings:**
• **{total_missing_pct:.1f}%** of your overall data is missing
• **'{worst_col[0].replace('_', ' ').title()}'** is the most incomplete field ({worst_col[1]['percentage']:.1f}% missing)
• **{missing_info['problematic_rows']} records** are missing information in multiple fields

💡 **What This Means for Your Business:**
• Missing data can lead to incomplete reports and incorrect decisions
• Red bars (>50% missing) indicate fields that may not be useful for analysis
• Yellow/Orange bars (20-50% missing) suggest areas where data collection can be improved

🔧 **Recommended Actions:**
1. Review why certain fields are frequently left empty
2. Make important fields mandatory in your data entry system
3. Consider removing fields with >70% missing data from reports
"""
        
        return fig, insight
    
    def visualize_duplicate_analysis(self):
        """Show duplicate row analysis with clear explanations"""
        dup_info = self._detect_duplicates()
        
        # Create simple bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=['Unique Records', 'Duplicate Records'],
                y=[len(self.df) - dup_info['count'], dup_info['count']],
                marker_color=['lightgreen', 'salmon'],
                text=[len(self.df) - dup_info['count'], dup_info['count']],
                textposition='auto',
                texttemplate='%{text} records'
            )
        ])
        
        fig.update_layout(
            title="Duplicate Records Check",
            xaxis_title="Record Type",
            yaxis_title="Count",
            height=400
        )
        
        # Generate insight
        if dup_info['count'] == 0:
            insight = """✅ **Excellent News!**

Your data contains no duplicate records. Every row is unique, which means:
• Your data is clean and ready for analysis
• No risk of counting the same transaction/customer twice
• Reports and calculations will be accurate
"""
        else:
            insight = f"""⚠️ **Attention Needed!**

📊 **What This Chart Shows:**
This chart compares unique records (green) versus duplicate records (red) in your dataset.

🎯 **Key Findings:**
• Found **{dup_info['count']} duplicate records** ({dup_info['percentage']:.1f}% of total)
• These duplicates might inflate your numbers and skew results

💡 **What This Means for Your Business:**
• Duplicate records can lead to:
  - Inflated revenue/sales figures
  - Incorrect customer counts
  - Misleading trend analysis
  
🔧 **Recommended Action:**
Remove these duplicate records before generating reports or making business decisions. This will ensure accurate analysis.
"""
        
        return fig, insight
    
    def visualize_data_quality_score(self):
        """Create an overall data quality score visualization"""
        missing_info = self._detect_missing_patterns()
        dup_info = self._detect_duplicates()
        outlier_info = self._detect_outliers()
        
        # Calculate quality score
        total_cells = len(self.df) * len(self.df.columns)
        missing_cells = missing_info['total_missing_cells']
        completeness_score = ((total_cells - missing_cells) / total_cells) * 100
        
        uniqueness_score = ((len(self.df) - dup_info['count']) / len(self.df)) * 100
        
        # Accuracy score based on outliers
        total_outliers = sum(info['count'] for info in outlier_info.values())
        accuracy_score = max(0, 100 - (total_outliers / len(self.df) * 100))
        
        overall_score = (completeness_score * 0.4 + uniqueness_score * 0.3 + accuracy_score * 0.3)
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=overall_score,
            title={'text': "Overall Data Quality Score"},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightcoral"},
                    {'range': [50, 75], 'color': "lightyellow"},
                    {'range': [75, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig.update_layout(height=400)
        
        # Generate insight
        if overall_score >= 90:
            grade = "Excellent"
            emoji = "🌟"
        elif overall_score >= 75:
            grade = "Good"
            emoji = "✅"
        elif overall_score >= 60:
            grade = "Fair"
            emoji = "⚠️"
        else:
            grade = "Needs Improvement"
            emoji = "❌"
        
        insight = f"""{emoji} **Data Quality Grade: {grade}**

📊 **What This Score Means:**
Your overall data quality score is **{overall_score:.1f}/100**

🎯 **Score Breakdown:**
• **Completeness:** {completeness_score:.1f}% - How much data you have vs. missing
• **Uniqueness:** {uniqueness_score:.1f}% - How many records are duplicates
• **Accuracy:** {accuracy_score:.1f}% - How many unusual values exist

💡 **What This Means for Your Business:**
"""
        
        if overall_score >= 80:
            insight += "Your data is reliable and ready for business decisions. Continue maintaining these standards!"
        elif overall_score >= 60:
            insight += "Your data is usable but has some issues. Address missing values and duplicates to improve reliability."
        else:
            insight += "⚠️ Your data needs significant cleanup before using it for important decisions. Focus on completing missing fields and removing duplicates."
        
        return fig, insight