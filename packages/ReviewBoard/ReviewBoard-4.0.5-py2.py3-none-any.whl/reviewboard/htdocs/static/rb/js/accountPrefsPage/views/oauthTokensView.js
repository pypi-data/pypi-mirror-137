"use strict";

(function () {
  var xhrUnknownErrorText = gettext("An unexpected error occurred. Could not delete OAuth2 token.");
  /**
   * A model representing an OAuth token.
   */

  var OAuthTokenItem = Djblets.Config.ListItem.extend({
    defaults: _.defaults({
      apiURL: '',
      application: '',
      showRemove: true
    }, Djblets.Config.ListItem.prototype.defaults)
  });
  /**
   * A view representing a single OAuthTokenItem.
   */

  var OAuthTokenItemView = Djblets.Config.ListItemView.extend({
    template: _.template("<span class=\"config-token-name\"><%- application %></span>"),
    actionHandlers: {
      'delete': '_onDeleteClicked'
    },

    /**
     * Delete the OAuth2 token.
     */
    _onDeleteClicked: function _onDeleteClicked() {
      var _this = this;

      RB.apiCall({
        url: this.model.get('apiURL'),
        method: 'DELETE',
        success: function success() {
          return _this.model.trigger('destroy');
        },
        error: function error(xhr) {
          return alert(xhr.errorText || xhrUnknownErrorText);
        }
      });
    }
  });
  /**
   * A view for managing OAuth2 tokens.
   */

  RB.OAuthTokensView = Backbone.View.extend({
    template: _.template("<div class=\"oauth-token-list\">\n <div class=\"djblets-l-config-forms-container -is-top-flush\">\n  <%- emptyText %>\n </div>\n</div>"),

    /**
     * Initialize the view.
     *
     * Args:
     *     options (object):
     *         The view options.
     *
     * Option Args:
     *     tokens (array of object):
     *         The serialized token attributes.
     */
    initialize: function initialize(options) {
      this.collection = new Backbone.Collection(options.tokens, {
        model: OAuthTokenItem
      });
    },

    /**
     * Render the view.
     *
     * Returns:
     *     RB.OAuthTokensView:
     *     This view.
     */
    render: function render() {
      this.$el.html(this.template({
        emptyText: gettext("You do not have any OAuth2 tokens.")
      }));
      this._$list = this.$('.oauth-token-list');
      this._listView = new Djblets.Config.ListView({
        ItemView: OAuthTokenItemView,
        model: new Djblets.Config.List({}, {
          collection: this.collection
        })
      });

      this._listView.render().$el.prependTo(this._$list);

      return this;
    }
  });
})();

//# sourceMappingURL=oauthTokensView.js.map