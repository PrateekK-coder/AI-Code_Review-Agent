from app.services.repository_review_service import RepositoryReviewService


def main():

    service = RepositoryReviewService()

    result = service.review_repository(
        github_url="https://github.com/HimanshuS-coder/Newsly.git",
        branch="main"
    )

    print("\n" + "=" * 80)
    print("FINAL REPOSITORY REVIEW")
    print("=" * 80)

    print("Files reviewed:", result["files_reviewed"])
    print("Total issues:", result["total_issues"])
    print("Severity counts:", result["severity_counts"])

    for issue in result["issues"]:

        print("\n" + "-" * 80)

        print("Category:", issue.category)
        print("Severity:", issue.severity)
        print("File:", issue.file)
        print("Line:", issue.line)
        print("Description:", issue.description)
        print("Recommendation:", issue.recommendation)


if __name__ == "__main__":
    main()