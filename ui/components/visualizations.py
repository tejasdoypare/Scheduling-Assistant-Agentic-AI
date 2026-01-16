"""
Visualization components using Plotly for the Scheduling Assistant.
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd


def create_negotiation_timeline(history: List[Dict]) -> go.Figure:
    """
    Create a timeline visualization of the negotiation process.
    
    Args:
        history: List of negotiation rounds with proposals and responses
        
    Returns:
        Plotly figure object
    """
    if not history:
        fig = go.Figure()
        fig.add_annotation(
            text="No negotiation history available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    rounds = []
    statuses = []
    colors = []
    
    for idx, round_data in enumerate(history, 1):
        rounds.append(f"Round {idx}")
        
        # Determine status
        if round_data.get('consensus_reached'):
            statuses.append("Consensus")
            colors.append("green")
        elif round_data.get('proposals'):
            statuses.append("Negotiating")
            colors.append("orange")
        else:
            statuses.append("No Agreement")
            colors.append("red")
    
    fig = go.Figure(data=[
        go.Bar(
            x=rounds,
            y=[1] * len(rounds),
            marker_color=colors,
            text=statuses,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Status: %{text}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Negotiation Progress Timeline",
        xaxis_title="Negotiation Round",
        yaxis_title="",
        yaxis_visible=False,
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def create_participant_responses(result: Dict) -> go.Figure:
    """
    Create a pie chart showing participant response distribution.
    
    Args:
        result: Negotiation result with participant responses
        
    Returns:
        Plotly figure object
    """
    # Count response types
    responses = {'Accepted': 0, 'Rejected': 0, 'Counter-proposed': 0}
    
    if 'history' in result:
        for round_data in result['history']:
            if 'participant_responses' in round_data:
                for response in round_data['participant_responses'].values():
                    if response.get('accept'):
                        responses['Accepted'] += 1
                    elif response.get('counter_proposal'):
                        responses['Counter-proposed'] += 1
                    else:
                        responses['Rejected'] += 1
    
    # Filter out zero values
    labels = [k for k, v in responses.items() if v > 0]
    values = [v for v in responses.values() if v > 0]
    
    if not values:
        fig = go.Figure()
        fig.add_annotation(
            text="No participant responses available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    colors = ['#2ecc71', '#e74c3c', '#f39c12'][:len(labels)]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Participant Response Distribution",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def create_confidence_evolution(history: List[Dict]) -> go.Figure:
    """
    Create a line chart showing confidence score evolution across rounds.
    
    Args:
        history: List of negotiation rounds
        
    Returns:
        Plotly figure object
    """
    if not history:
        fig = go.Figure()
        fig.add_annotation(
            text="No confidence data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    rounds = []
    confidence_scores = []
    
    for idx, round_data in enumerate(history, 1):
        rounds.append(idx)
        
        # Extract confidence from top proposal
        if 'proposals' in round_data and round_data['proposals']:
            top_proposal = round_data['proposals'][0]
            confidence = top_proposal.get('confidence_score', 0)
            confidence_scores.append(confidence * 100)  # Convert to percentage
        else:
            confidence_scores.append(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=rounds,
        y=confidence_scores,
        mode='lines+markers',
        name='Confidence',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10),
        hovertemplate='<b>Round %{x}</b><br>Confidence: %{y:.1f}%<extra></extra>'
    ))
    
    # Add threshold line
    fig.add_hline(
        y=70,
        line_dash="dash",
        line_color="green",
        annotation_text="Target: 70%",
        annotation_position="right"
    )
    
    fig.update_layout(
        title="Confidence Score Evolution",
        xaxis_title="Negotiation Round",
        yaxis_title="Confidence Score (%)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=40),
        yaxis_range=[0, 100]
    )
    
    return fig


def create_timezone_distribution(calendars: Dict) -> go.Figure:
    """
    Create a bar chart showing participant distribution across timezones.
    
    Args:
        calendars: Dictionary of participant calendars with timezone info
        
    Returns:
        Plotly figure object
    """
    timezones = {}
    
    for name, calendar in calendars.items():
        tz = calendar.get('timezone', 'UTC')
        timezones[tz] = timezones.get(tz, 0) + 1
    
    if not timezones:
        fig = go.Figure()
        fig.add_annotation(
            text="No timezone data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(timezones.keys()),
            y=list(timezones.values()),
            marker_color='#9b59b6',
            text=list(timezones.values()),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Participants: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Participant Timezone Distribution",
        xaxis_title="Timezone",
        yaxis_title="Number of Participants",
        height=400,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    return fig


def create_slot_comparison(proposals: List[Dict]) -> go.Figure:
    """
    Create a horizontal bar chart comparing proposed time slots.
    
    Args:
        proposals: List of time slot proposals with confidence scores
        
    Returns:
        Plotly figure object
    """
    if not proposals:
        fig = go.Figure()
        fig.add_annotation(
            text="No proposals available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Limit to top 5 proposals
    top_proposals = proposals[:5]
    
    slots = []
    scores = []
    colors = []
    
    for idx, proposal in enumerate(top_proposals, 1):
        start = proposal.get('start', 'Unknown')
        slots.append(f"Slot {idx}: {start}")
        score = proposal.get('confidence_score', 0) * 100
        scores.append(score)
        
        # Color based on score
        if score >= 70:
            colors.append('#2ecc71')  # Green
        elif score >= 50:
            colors.append('#f39c12')  # Orange
        else:
            colors.append('#e74c3c')  # Red
    
    fig = go.Figure(data=[
        go.Bar(
            y=slots,
            x=scores,
            orientation='h',
            marker_color=colors,
            text=[f"{s:.1f}%" for s in scores],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Confidence: %{x:.1f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Top Time Slot Proposals",
        xaxis_title="Confidence Score (%)",
        yaxis_title="",
        height=300,
        margin=dict(l=20, r=20, t=40, b=40),
        xaxis_range=[0, 100]
    )
    
    return fig


def create_negotiation_summary_stats(result: Dict) -> Dict[str, Any]:
    """
    Calculate summary statistics for the negotiation.
    
    Args:
        result: Negotiation result dictionary
        
    Returns:
        Dictionary with summary statistics
    """
    stats = {
        'total_rounds': result.get('rounds_completed', 0),
        'success': result.get('success', False),
        'consensus_reached': result.get('consensus_reached', False),
        'final_confidence': result.get('confidence_score', 0) * 100,
        'total_proposals': 0,
        'total_responses': 0,
        'acceptance_rate': 0
    }
    
    if 'history' in result:
        accepted = 0
        total_responses = 0
        
        for round_data in result['history']:
            if 'proposals' in round_data:
                stats['total_proposals'] += len(round_data['proposals'])
            
            if 'participant_responses' in round_data:
                for response in round_data['participant_responses'].values():
                    total_responses += 1
                    if response.get('accept'):
                        accepted += 1
        
        stats['total_responses'] = total_responses
        if total_responses > 0:
            stats['acceptance_rate'] = (accepted / total_responses) * 100
    
    return stats
