from app.services.repository_review_service import RepositoryReviewService


service = RepositoryReviewService()


result = service.review_repository(
    github_url="https://github.com/PrateekK-coder/Wish_List-App.git",
    branch="main"
)


print("\n" + "=" * 80)
print("FINAL RESULT")
print("=" * 80)

print(result)