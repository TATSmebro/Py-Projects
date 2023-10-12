import flet as ft
import praw


reddit = praw.Reddit(
    client_id="AJAS0I-QOAzK5tSFf6NRXA",  # Change this to your Client ID
    client_secret="5_laSMwGCUnxzDWm3paq4-69ULWTzg",  # Change this to your Client Secret
    password="marcus0612",  # Change this to your Reddit account password
    user_agent="testscript by u/ShoppingWilling9640",  # Change this to "testscript by u/(your username)"
    username="ShoppingWilling9640",  # Change this to your username
)


def main(page):
    page.title = "CS 150 23.1 Lab 1"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # For layouting; ignore

    controls = [post for post in reddit.front.new()]
    posts = reddit.front.new()

    def handle_upvote(post, idx):
        def upvote_arrow_click(_):
            if post.likes:
                print(f'Clearing vote for post: {post.title}')
                post.clear_vote()
                post.likes = None
                post.score -= 1
            else:
                print(f'Upvoting post: {post.title}')
                post.upvote()

                if post.likes == False:
                    post.score += 2
                else:
                    post.score += 1

                post.likes = True

            update_post(post, idx)

        return upvote_arrow_click

    def handle_downvote(post, idx):
        def downvote_arrow_click(_):
            if post.likes is False:
                print(f'Clearing vote for post: {post.title}')
                post.clear_vote()
                post.likes = None
                post.score += 1
            else:
                print(f'Downvoting post: {post.title}')
                post.downvote()

                if post.likes:
                    post.score -= 2
                else:
                    post.score -= 1

                post.likes = False

            update_post(post, idx)

        return downvote_arrow_click
    
    def update_post(post, idx):
        upvote_arrow_click = handle_upvote(post, idx)
        downvote_arrow_click = handle_downvote(post, idx)

        upvote_arrow = ft.IconButton(
            icon='arrow_upward',
            icon_color='orange' if post.likes else 'grey',
            on_click=upvote_arrow_click,
        )

        score_text = ft.Text(
            str(post.score),
            color='orange' if post.likes else 'blue' if post.likes is False else 'grey',
        )

        downvote_arrow = ft.IconButton(
            icon='arrow_downward',
            icon_color='blue' if post.likes is False else 'grey',
            on_click=downvote_arrow_click,
        )

        controls[idx] = ft.Card(
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            upvote_arrow,
                                            score_text,
                                            downvote_arrow,
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        width=80,     # For layouting; ignore
                                    ),
                                    ft.Text(
                                        post.title,
                                        max_lines=2,  # For layouting; ignore
                                        expand=1,     # For layouting; ignore
                                    ),
                                ],
                            ),
                        )
        
        page.update()

    for idx, post in enumerate(posts):
        update_post(post, idx)


    page.add(
        ft.ListView(
            controls,
            expand=1,    # For layouting; ignore
            spacing=10,  # For layouting; ignore
            padding=20,  # For layouting; ignore
        )
    )


ft.app(target=main)
