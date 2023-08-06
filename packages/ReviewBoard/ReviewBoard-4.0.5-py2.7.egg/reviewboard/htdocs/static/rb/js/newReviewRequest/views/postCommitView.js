"use strict";

/**
 * A view orchestrating post-commit review request creation.
 *
 * This brings together the BranchesView and CommitsView to provide a UI for
 * letting people browse through the committed revisions in the repository. When
 * the user clicks on one of the commits, it will create a new review request
 * using that commit's ID.
 */
RB.PostCommitView = Backbone.View.extend({
  className: 'post-commit',
  loadErrorTemplate: _.template("<div class=\"error\">\n <p><%- errorLoadingText %></p>\n <p class=\"error-text\">\n  <% _.each(errorLines, function(line) { %><%- line %><br /><% }); %>\n </p>\n <p>\n  <%- temporaryFailureText %>\n  <a href=\"#\" id=\"reload_<%- reloadID %>\"><%- tryAgainText %></a>\n </p>\n</div>"),
  events: {
    'click #reload_branches': '_loadBranches',
    'click #reload_commits': '_loadCommits'
  },

  /**
   * Initialize the view.
   *
   * Args:
   *     options (object):
   *         Options for the view.
   *
   * Option Args:
   *     $scrollContainer (jQuery):
   *         The parent container handling all content scrolling.
   */
  initialize: function initialize(options) {
    var model = this.model;
    var repository = model.get('repository');
    var branches = repository.branches;
    this._$scrollContainer = options.$scrollContainer;
    this._$error = null; // Set up the branch selector and bind it to the "branch" attribute

    this._branchesView = new RB.BranchesView({
      collection: branches
    });

    this._branchesView.on('selected', function (branch) {
      return model.set('branch', branch);
    });

    this.listenTo(model, 'change:branch', this._onBranchChanged);

    if (!branches.loaded) {
      this._loadBranches();
    }
  },

  /**
   * Render the view.
   *
   * Returns:
   *     RB.PostCommitView:
   *     This object, for chaining.
   */
  render: function render() {
    this._rendered = true;
    $('<div/>').addClass('branches section-header').append($('<span/>').text(gettext("Create from an existing commit on:"))).append(this._branchesView.render().el).appendTo(this.$el);

    if (this._commitsView) {
      this.$el.append(this._commitsView.render().el);
    }

    return this;
  },

  /**
   * Load the list of branches from the repository.
   *
   * If there's an error loading the branches, the branches selector and
   * commits list will be hidden, and an error will be displayed along
   * with the message from the server. The user will have the ability to
   * try again.
   */
  _loadBranches: function _loadBranches() {
    var _this = this;

    this._clearLoadError();

    var branches = this.model.get('repository').branches;
    branches.fetch({
      success: function success() {
        branches.loaded = true;

        _this._branchesView.$el.show();

        if (_this._commitsView) {
          _this._commitsView.$el.show();
        }
      },
      error: function error(collection, xhr) {
        _this._branchesView.$el.hide();

        if (_this._commitsView) {
          _this._commitsView.$el.hide();
        }

        _this._showLoadError('branches', xhr);
      }
    });
  },

  /**
   * Load the list of commits from the repository.
   *
   * If there's an error loading the commits, the commits list will be
   * hidden, and an error will be displayed along with the message from
   * the server. The user will have the ability to try again.
   */
  _loadCommits: function _loadCommits() {
    var _this2 = this;

    this._clearLoadError();

    this._commitsCollection.fetch({
      success: function success() {
        _this2._commitsView.$el.show();

        _this2._commitsView.checkFetchNext();
      },
      error: function error(collection, xhr) {
        _this2._commitsView.$el.hide();

        _this2._showLoadError('commits', xhr);
      }
    });
  },

  /**
   * Clear any displayed error message.
   */
  _clearLoadError: function _clearLoadError() {
    if (this._$error) {
      this._$error.remove();

      this._$error = null;
    }
  },

  /**
   * Show an error message indicating a load failure.
   *
   * The message from the server will be displayed along with some
   * helpful text and a link for trying the request again.
   *
   * Args:
   *     reloadID (string):
   *         An ID to use for the reload link element.
   *
   *     xhr (jqXHR):
   *         The HTTP Request object.
   */
  _showLoadError: function _showLoadError(reloadID, xhr) {
    this._clearLoadError();

    this._$error = $(this.loadErrorTemplate({
      errorLoadingText: gettext("There was an error loading information from this repository:"),
      temporaryFailureText: gettext("This may be a temporary failure."),
      tryAgainText: gettext("Try again"),
      errorLines: xhr.errorText.split('\n'),
      reloadID: reloadID
    })).appendTo(this.$el);
  },

  /**
   * Callback for when the user chooses a different branch.
   *
   * Fetches a new list of commits starting from the tip of the selected
   * branch.
   *
   * Args:
   *     model (RB.PostCommitModel):
   *         The data model.
   *
   *     branch (RB.RepositoryBranch):
   *         The selected branch.
   */
  _onBranchChanged: function _onBranchChanged(model, branch) {
    var _this3 = this;

    if (this._commitsView) {
      this.stopListening(this._commitsCollection);

      this._commitsView.remove();
    }

    this._commitsCollection = this.model.get('repository').getCommits({
      branch: branch.id,
      start: branch.get('commit')
    });
    this.listenTo(this._commitsCollection, 'create', this._onCreateReviewRequest);
    this._commitsView = new RB.CommitsView({
      collection: this._commitsCollection,
      $scrollContainer: this._$scrollContainer
    });
    this.listenTo(this._commitsView, 'loadError', function (xhr) {
      _this3._showLoadError('commits', xhr);
    });

    if (this._rendered) {
      this.$el.append(this._commitsView.render().el);
    }

    this._loadCommits();
  },

  /**
   * Callback for when a commit is selected.
   *
   * Creates a new review request with the given commit ID and redirects the
   * browser to it.
   *
   * Args:
   *     commit (RB.RepositoryCommit):
   *         The selected commit.
   */
  _onCreateReviewRequest: function _onCreateReviewRequest(commit) {
    var _this4 = this;

    if (this._createPending) {
      // Do nothing
      return;
    }

    this._createPending = true;

    this._commitsView.setPending(commit);

    var repository = this.model.get('repository');
    var reviewRequest = new RB.ReviewRequest({
      repository: repository.id,
      localSitePrefix: repository.get('localSitePrefix')
    });
    reviewRequest.createFromCommit({
      commitID: commit.id,
      success: function success() {
        window.location = reviewRequest.get('reviewURL');
      },
      error: function error(model, xhr) {
        _this4._commitsView.setPending(null);

        _this4._createPending = false;
        alert(xhr.errorText);
      }
    });
  }
});

//# sourceMappingURL=postCommitView.js.map