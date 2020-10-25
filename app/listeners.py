import re

from slack_bolt import App

from app.onboarding import (
    message_multi_users_select,
    message_multi_users_select_lazy,
)
from app.tutorials import (
    tutorial_page_transition,
    tutorial_page_transition_lazy,
    app_home_opened,
    app_home_opened_lazy,
    page1_home_tab_button_click,
    page1_home_tab_button_click_lazy,
    page1_home_tab_users_select_lazy,
    page1_home_tab_users_select,
    page2_modal,
    page2_modal_lazy,
    page2_modal_submission,
    page4_create_channel,
    page4_create_channel_lazy,
    page4_create_channel_submission,
    page4_create_channel_setup,
    page4_create_channel_setup_lazy,
    global_shortcut_handler,
    global_shortcut_view_submission,
    global_shortcut_view_submission_lazy,
    message_shortcut_handler,
    message_shortcut_handler_lazy,
    external_data_source_handler,
)


def register_listeners(app: App):
    app.action("link_button")(lambda ack: ack())

    # ----------------------------------------------
    # message

    app.action("message_multi_users_select")(
        ack=message_multi_users_select, lazy=[message_multi_users_select_lazy]
    )

    # ----------------------------------------------
    # home tab

    app.event("app_home_opened")(ack=app_home_opened, lazy=[app_home_opened_lazy])

    app.action(re.compile("tutorial_page_transition_\d+"))(
        ack=tutorial_page_transition, lazy=[tutorial_page_transition_lazy]
    )

    app.action(re.compile("page1_home_tab_button_\d"))(
        ack=page1_home_tab_button_click, lazy=[page1_home_tab_button_click_lazy]
    )

    app.action("page1_home_tab_users_select")(
        ack=page1_home_tab_users_select, lazy=[page1_home_tab_users_select_lazy]
    )

    app.action("page2_modal")(ack=page2_modal, lazy=[page2_modal_lazy])

    app.view("page2_modal_submission")(page2_modal_submission)

    app.action("page4_create_channel")(
        ack=page4_create_channel, lazy=[page4_create_channel_lazy]
    )

    app.view("page4_create_channel_submission")(page4_create_channel_submission)
    app.event("channel_created")(
        ack=page4_create_channel_setup, lazy=[page4_create_channel_setup_lazy]
    )

    app.shortcut("global-shortcut-example")(global_shortcut_handler)

    app.view("global-shortcut-example_submission")(
        ack=global_shortcut_view_submission, lazy=[global_shortcut_view_submission_lazy]
    )

    app.shortcut("message-shortcut-example")(
        ack=message_shortcut_handler, lazy=[message_shortcut_handler_lazy]
    )

    app.options("external-data-source-example")(external_data_source_handler)
    app.action("external-data-source-example")(lambda ack: ack())
