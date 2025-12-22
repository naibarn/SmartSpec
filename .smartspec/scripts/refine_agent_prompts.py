#!/usr/bin/env python3
"""
SmartSpec Agent Prompt Refiner
Analyzes UI analytics and suggests prompt improvements
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


class PromptRefiner:
    """Refines AI agent prompts based on analytics"""
    
    def __init__(self):
        self.analytics: Dict[str, Any] = {}
        self.suggestions: List[Dict[str, Any]] = []
        
    def load_analytics(self, analytics_file: str) -> Dict[str, Any]:
        """Load analytics data from file"""
        with open(analytics_file, 'r', encoding='utf-8') as f:
            self.analytics = json.load(f)
        
        return self.analytics
    
    def analyze(self, focus_area: str = "all", threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Analyze analytics and generate refinement suggestions"""
        self.suggestions = []
        
        # Get metrics
        metrics = self.analytics.get("summary", {}).get("metrics", {})
        issues = self.analytics.get("issues", [])
        
        # Analyze based on focus area
        if focus_area in ["all", "accessibility"]:
            self._analyze_accessibility(metrics, issues, threshold)
        
        if focus_area in ["all", "performance"]:
            self._analyze_performance(metrics, issues, threshold)
        
        if focus_area in ["all", "engagement"]:
            self._analyze_engagement(metrics, issues, threshold)
        
        if focus_area in ["all", "usability"]:
            self._analyze_usability(metrics, issues, threshold)
        
        # Sort by confidence and impact
        self.suggestions.sort(key=lambda x: (x["confidence"], x["impact"]), reverse=True)
        
        return self.suggestions
    
    def _analyze_accessibility(self, metrics: Dict[str, Any], issues: List[Dict], threshold: float) -> None:
        """Analyze accessibility metrics"""
        accessibility_score = metrics.get("accessibility_score", 1.0)
        
        # Check for missing alt text
        missing_alt_count = sum(1 for issue in issues if "alt" in issue.get("description", "").lower())
        total_images = metrics.get("total_components", 0)
        
        if total_images > 0:
            missing_alt_rate = missing_alt_count / total_images
            
            if missing_alt_rate > 0.2:  # More than 20% missing alt text
                confidence = min(0.95, missing_alt_rate * 1.2)
                
                if confidence >= threshold:
                    self.suggestions.append({
                        "issue_type": "accessibility",
                        "issue": "Missing Alt Text",
                        "description": f"{int(missing_alt_rate * 100)}% of images are missing alt text",
                        "current_prompt": "Generate a component with image",
                        "refined_prompt": "Generate a component with image. IMPORTANT: Include descriptive alt text for all images (WCAG 2.1 Level AA compliance). Alt text should describe the image content and purpose.",
                        "expected_impact": f"+{int(missing_alt_rate * 100)}% accessibility score",
                        "confidence": confidence,
                        "priority": "high"
                    })
        
        # Check for low contrast
        if accessibility_score < 0.7:
            confidence = 0.85
            
            if confidence >= threshold:
                self.suggestions.append({
                    "issue_type": "accessibility",
                    "issue": "Low Color Contrast",
                    "description": f"Accessibility score is {accessibility_score:.2f}, indicating potential contrast issues",
                    "current_prompt": "Use colors from theme",
                    "refined_prompt": "Use colors from theme. IMPORTANT: Ensure text-background contrast meets WCAG AA standards (4.5:1 for normal text, 3:1 for large text). Use theme tokens with sufficient contrast.",
                    "expected_impact": f"+{int((1 - accessibility_score) * 50)}% accessibility score",
                    "confidence": confidence,
                    "priority": "high"
                })
    
    def _analyze_performance(self, metrics: Dict[str, Any], issues: List[Dict], threshold: float) -> None:
        """Analyze performance metrics"""
        avg_load_time = metrics.get("avg_load_time", 0)
        
        if avg_load_time > 3.0:  # Load time > 3 seconds
            confidence = min(0.90, (avg_load_time - 3.0) / 5.0 + 0.7)
            
            if confidence >= threshold:
                self.suggestions.append({
                    "issue_type": "performance",
                    "issue": "High Load Time",
                    "description": f"Average load time is {avg_load_time:.1f}s (target: <3s)",
                    "current_prompt": "Generate a dashboard with all features",
                    "refined_prompt": "Generate a dashboard with progressive loading. Use lazy loading for below-fold components. Limit initial render to 10 components max. Defer non-critical features.",
                    "expected_impact": f"-{int((avg_load_time - 3.0) / avg_load_time * 100)}% load time",
                    "confidence": confidence,
                    "priority": "medium"
                })
        
        # Check component complexity
        total_components = metrics.get("total_components", 0)
        
        if total_components > 50:
            confidence = 0.75
            
            if confidence >= threshold:
                self.suggestions.append({
                    "issue_type": "performance",
                    "issue": "High Component Count",
                    "description": f"Page has {total_components} components, which may impact performance",
                    "current_prompt": "Generate all components for the page",
                    "refined_prompt": "Generate components with virtualization for long lists. Use pagination or infinite scroll for large datasets. Limit visible components to 20-30 per viewport.",
                    "expected_impact": "-20% render time",
                    "confidence": confidence,
                    "priority": "low"
                })
    
    def _analyze_engagement(self, metrics: Dict[str, Any], issues: List[Dict], threshold: float) -> None:
        """Analyze engagement metrics"""
        click_rate = metrics.get("click_rate", 0)
        
        if click_rate < 0.3:  # Click rate < 30%
            confidence = 0.80
            
            if confidence >= threshold:
                self.suggestions.append({
                    "issue_type": "engagement",
                    "issue": "Low Click Rate",
                    "description": f"Click rate is {click_rate * 100:.1f}% (target: >30%)",
                    "current_prompt": "Generate a button for the action",
                    "refined_prompt": "Generate a button for the action with clear, action-oriented label. Use primary variant for main actions. Add visual hierarchy with size and color. Consider adding icons for better recognition.",
                    "expected_impact": f"+{int((0.3 - click_rate) * 200)}% click rate",
                    "confidence": confidence,
                    "priority": "medium"
                })
        
        # Check interaction patterns
        interaction_count = metrics.get("total_interactions", 0)
        
        if interaction_count < 10:
            confidence = 0.70
            
            if confidence >= threshold:
                self.suggestions.append({
                    "issue_type": "engagement",
                    "issue": "Low Interaction Count",
                    "description": f"Only {interaction_count} interactive elements detected",
                    "current_prompt": "Generate a static page",
                    "refined_prompt": "Generate an interactive page with clear calls-to-action. Include buttons, links, and interactive elements. Add hover states and feedback for better UX.",
                    "expected_impact": "+50% user engagement",
                    "confidence": confidence,
                    "priority": "low"
                })
    
    def _analyze_usability(self, metrics: Dict[str, Any], issues: List[Dict], threshold: float) -> None:
        """Analyze usability metrics"""
        error_rate = metrics.get("error_rate", 0)
        
        if error_rate > 0.1:  # Error rate > 10%
            confidence = 0.85
            
            if confidence >= threshold:
                self.suggestions.append({
                    "issue_type": "usability",
                    "issue": "High Error Rate",
                    "description": f"Error rate is {error_rate * 100:.1f}% (target: <10%)",
                    "current_prompt": "Generate a form with input fields",
                    "refined_prompt": "Generate a form with input fields. Include clear labels, placeholder text, and validation hints. Add error messages with specific guidance. Use appropriate input types (email, tel, etc.).",
                    "expected_impact": f"-{int(error_rate * 100)}% error rate",
                    "confidence": confidence,
                    "priority": "high"
                })
        
        # Check for theme consistency
        theme_violations = sum(1 for issue in issues if "theme" in issue.get("description", "").lower())
        
        if theme_violations > 5:
            confidence = 0.88
            
            if confidence >= threshold:
                self.suggestions.append({
                    "issue_type": "usability",
                    "issue": "Theme Inconsistency",
                    "description": f"{theme_violations} components not using theme tokens",
                    "current_prompt": "Generate a component with custom styles",
                    "refined_prompt": "Generate a component using theme tokens. IMPORTANT: Always reference theme tokens (e.g., {colors.primary.500}) instead of hardcoding values. Use predefined component variants from theme.",
                    "expected_impact": "+30% design consistency",
                    "confidence": confidence,
                    "priority": "medium"
                })
    
    def generate_report(self, output_format: str = "markdown", include_examples: bool = True) -> str:
        """Generate refinement report"""
        if output_format == "markdown":
            return self._generate_markdown_report(include_examples)
        elif output_format == "json":
            return json.dumps({
                "generated_at": datetime.now().isoformat(),
                "total_suggestions": len(self.suggestions),
                "suggestions": self.suggestions
            }, indent=2, ensure_ascii=False)
        else:
            return ""
    
    def _generate_markdown_report(self, include_examples: bool) -> str:
        """Generate markdown report"""
        lines = [
            "# AI Agent Prompt Refinement Suggestions",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Suggestions:** {len(self.suggestions)}",
            ""
        ]
        
        # Group by issue type
        by_type = {}
        for suggestion in self.suggestions:
            issue_type = suggestion["issue_type"]
            if issue_type not in by_type:
                by_type[issue_type] = []
            by_type[issue_type].append(suggestion)
        
        # Generate sections
        for issue_type, suggestions in by_type.items():
            lines.append(f"## {issue_type.title()} Refinements")
            lines.append("")
            
            for i, suggestion in enumerate(suggestions, 1):
                lines.append(f"### {i}. {suggestion['issue']}")
                lines.append("")
                lines.append(f"**Description:** {suggestion['description']}")
                lines.append("")
                lines.append("**Current Prompt Pattern:**")
                lines.append(f"```")
                lines.append(suggestion['current_prompt'])
                lines.append("```")
                lines.append("")
                lines.append("**Refined Prompt:**")
                lines.append(f"```")
                lines.append(suggestion['refined_prompt'])
                lines.append("```")
                lines.append("")
                lines.append(f"**Expected Impact:** {suggestion['expected_impact']}")
                lines.append(f"**Confidence:** {suggestion['confidence']:.2f}")
                lines.append(f"**Priority:** {suggestion['priority']}")
                lines.append("")
                lines.append("---")
                lines.append("")
        
        return "\n".join(lines)
    
    def save_report(self, output_file: str, content: str) -> None:
        """Save report to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartSpec Agent Prompt Refiner")
    parser.add_argument("--analytics-file", required=True)
    parser.add_argument("--focus-area", default="all", choices=["all", "accessibility", "performance", "engagement", "usability"])
    parser.add_argument("--output-format", default="markdown", choices=["markdown", "json", "both"])
    parser.add_argument("--output-file", default=".spec/prompt_refinements.md")
    parser.add_argument("--threshold", type=float, default=0.7)
    parser.add_argument("--include-examples", type=bool, default=True)
    parser.add_argument("--auto-apply", type=bool, default=False)
    
    args = parser.parse_args()
    
    refiner = PromptRefiner()
    
    try:
        # Load analytics
        print(f"📊 Loading analytics from {args.analytics_file}...")
        refiner.load_analytics(args.analytics_file)
        
        # Analyze
        print(f"🔍 Analyzing {args.focus_area} metrics...")
        suggestions = refiner.analyze(args.focus_area, args.threshold)
        
        print(f"✅ Found {len(suggestions)} refinement suggestions")
        
        # Generate report
        if args.output_format in ["markdown", "both"]:
            print(f"📝 Generating markdown report...")
            markdown_report = refiner.generate_report("markdown", args.include_examples)
            
            output_file = args.output_file
            if args.output_format == "both" and not output_file.endswith(".md"):
                output_file = output_file.replace(".json", ".md")
            
            refiner.save_report(output_file, markdown_report)
            print(f"✅ Saved markdown report to {output_file}")
        
        if args.output_format in ["json", "both"]:
            print(f"📝 Generating JSON report...")
            json_report = refiner.generate_report("json")
            
            json_file = args.output_file.replace(".md", ".json")
            refiner.save_report(json_file, json_report)
            print(f"✅ Saved JSON report to {json_file}")
        
        # Auto-apply (placeholder)
        if args.auto_apply:
            high_confidence = [s for s in suggestions if s["confidence"] >= 0.9]
            print(f"🤖 Auto-apply enabled: {len(high_confidence)} high-confidence suggestions would be applied")
            print("⚠️  Note: Auto-apply is not yet implemented in this version")
        
        # Print summary
        print("\n📊 Summary:")
        print(f"   Total suggestions: {len(suggestions)}")
        print(f"   High priority: {sum(1 for s in suggestions if s['priority'] == 'high')}")
        print(f"   Medium priority: {sum(1 for s in suggestions if s['priority'] == 'medium')}")
        print(f"   Low priority: {sum(1 for s in suggestions if s['priority'] == 'low')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
