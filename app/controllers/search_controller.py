from app.utils.session import Session
from app.services.search_service import SearchService


class SearchController:
    """
    Handles search and save logic.
    Receives the shared Session — uses session.user_id when
    saving anything to the models so records are tied to the
    correct user.
    """

    def __init__(self, session: Session, search_view, text_view):
        self.session = session
        self.search_view = search_view
        self.text_view = text_view
        self.on_search_typed("")

        # Wire up panel signals
        search_view.result_selected.connect(self.on_result_selected)
        search_view.search_changed.connect(self.on_search_typed)
        #text_view.save_requested.connect(self.on_save)

    # ── Search ────────────────────────────────────────────────────────────────

    def on_search_typed(self, text: str):
        print("executing search with text:", text)

        if not text.strip():
            print("blank search")
            posts = SearchService.search_by_id(
                user_id=self.session.user_id
            )
            print(posts)
            self.search_view.set_results(posts)
        else:
            # Only search records belonging to the logged-in user
            posts = SearchService.search_by_title(
                query=text,
                user_id=self.session.user_id
            )
            self.search_view.set_results(posts)


    def on_result_selected(self, post_id: int):
        """
        Receives the post ID emitted by the search panel.
        Fetches the full post from the DB and loads it into the text panel.
        """
        post = SearchService.get_by_id(
            post_id=post_id,
            user_id=self.session.user_id
        )
        if post is None:
            return

        self.text_view.set_title(post.title)
        self.text_view.set_content(post.content)

    # ── Save ──────────────────────────────────────────────────────────────────

    def on_save(self, title: str, content: str):
        """
        Save button pressed in the text panel.
        user_id is injected from the session — the view never
        needs to know who is logged in.
        """
        SearchService.save(
            title=title,
            content=content,
            user_id=self.session.user_id
        )
        self.search_view.set_results(
            SearchService.all_for_user(self.session.user_id)
        )