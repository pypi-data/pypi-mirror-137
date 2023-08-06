"use strict";

/**
 * A view that lists a series of commits.
 *
 * This is intended to be used for creating new review requests from committed
 * revisions. The containing view can call setPending/cancelPending to ask an
 * individual commit to show a spinner.
 */
RB.CommitsView = RB.CollectionView.extend({
  className: 'commits',
  itemViewType: RB.CommitView,

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
    RB.CollectionView.prototype.initialize.call(this, options);
    this._$scrollContainer = options.$scrollContainer;
    this._fetchingCommits = false;
  },

  /**
   * Render the view.
   *
   * Delegates the hard work to the parent class, and sets up the scroll
   * handler.
   *
   * Returns:
   *     RB.CommitsView:
   *     This object, for chaining.
   */
  render: function render() {
    RB.CollectionView.prototype.render.call(this);

    this._$scrollContainer.scroll(this.checkFetchNext.bind(this));

    return this;
  },

  /**
   * Set a given commit "pending".
   *
   * This is used while creating a new review request, and will ask the
   * correct commit view to show a spinner.
   *
   * Args:
   *     commit (RB.RepositoryCommit):
   *         The selected commit.
   */
  setPending: function setPending(commit) {
    this.views.forEach(function (view) {
      if (view.model === commit) {
        view.showProgress();
      } else {
        view.cancelProgress();
      }
    });
  },

  /**
   * Cancel the pending state on all commits.
   */
  cancelPending: function cancelPending() {
    this.views.forEach(function (view) {
      return view.cancelProgress();
    });
  },

  /**
   * Check whether we need to fetch more commits.
   *
   * Commits need to be fetched if the scroll container hasn't been filled
   * yet (due to too few commits for the available window height) or if
   * the user has scrolled close to the end of the scroll container.
   *
   * Once new commits have been fetched, they'll be rendered, and an
   * immediate check will be performed to see if we still need to fetch
   * more commits, in case the scroll container is still not filled.
   */
  checkFetchNext: function checkFetchNext() {
    var _this = this;

    if (this._fetchingCommits) {
      return;
    }

    var collection = this.collection;
    var scrollContainerEl = this._$scrollContainer[0];
    var scrollThresholdPx = 50;

    if (collection.canFetchNext() && scrollContainerEl.scrollTop + scrollContainerEl.offsetHeight > scrollContainerEl.scrollHeight - scrollThresholdPx) {
      this._fetchingCommits = true;
      collection.fetchNext({
        success: function success() {
          _this._fetchingCommits = false;

          if (collection.canFetchNext()) {
            /*
             * There may still be room left for more commits.
             * We need to populate past the scroll point, so
             * check again.
             */
            _this.checkFetchNext();
          }
        },
        error: function error(collection, xhr) {
          _this._fetchingCommits = false;

          _this.trigger('loadError', xhr);
        }
      });
    }
  }
});

//# sourceMappingURL=commitsView.js.map