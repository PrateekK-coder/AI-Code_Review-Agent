

class ReviewAgentAggregator:
    def aggregate(self, reviews):
       unique_issues = {}

       for review in reviews:

            for issue in review.issues:

                key = (
                issue.file,
                issue.line,
                issue.category,
                issue.description
                )

                unique_issues[key] = issue

       all_issues = list(unique_issues.values())
       print("Issues before deduplication:",
              sum(len(review.issues) for review in reviews))

       print("Issues after deduplication:",
              len(all_issues))
       severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

       for issue in all_issues:
            severity_counts[issue.severity] += 1

       return {
    "files_reviewed": len(reviews),
    "total_issues": len(all_issues),
    "severity_counts": severity_counts,
    "issues": all_issues
    }