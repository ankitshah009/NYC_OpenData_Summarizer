# Set up OpenAI API key
import openai
import pandas as pd
import matplotlib.pyplot as plt
import os
import json


# Access the API key from environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')


class Chatbot:
    def __init__(self):
        self.data = None  # Placeholder for your data

    def load_data(self, folder):
        data = {}
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                filepath = os.path.join(folder, filename)
                with open(filepath, 'r') as file:
                    data[filename] = json.load(file)
        self.data = data

    def analyze_data(self, dataset_name):
        # Assuming the data is tabular
        dataset = self.data.get(dataset_name, {})
        df = pd.DataFrame(dataset)
        
        # Rudimentary analysis: Summary statistics
        summary_stats = df.describe().T
        
        # Create a dashboard with a simple histogram for each numeric column
        figs = []
        for col in df.select_dtypes(include=['number']).columns:
            fig, ax = plt.subplots()
            df[col].hist(ax=ax)
            ax.set_title(f'Histogram of {col}')
            figs.append(fig)
        
        return summary_stats, figs

    def generate_response(self, dataset_name):
        analysis_result, dashboards = self.analyze_data(dataset_name)
        return analysis_result, dashboards

    def provide_insights(self):
        insights = []
        for dataset_name, dataset in self.data.items():
            df = pd.DataFrame(dataset)
            insights.append(f'{dataset_name}:')
            insights.append(f'- Number of records: {len(df)}')
            insights.append(f'- Number of columns: {len(df.columns)}')
            insights.append(f'- Columns: {", ".join(df.columns)}')
        return "\n".join(insights)
    
    def provide_insights_and_dashboards(self, folder):
        insights = []
        dashboards = []
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                filepath = os.path.join(folder, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                df = pd.DataFrame(data)
                
                # Generating Insights
                insight = {
                    'dataset_name': filename,
                    'number_of_records': len(df),
                    'number_of_columns': len(df.columns),
                    'columns': list(df.columns)
                }
                insights.append(insight)
                
                # Creating Dashboards
                for column in df.select_dtypes(include=['number']).columns:
                    fig, ax = plt.subplots()
                    df[column].plot(kind='hist', ax=ax)
                    ax.set_title(f'{filename} - {column}')
                    dashboards.append(fig)
        
        return insights, dashboards
