"use strict";

/**
 * Models the dashboard and its operations.
 *
 * This will keep track of any selected review requests, and can
 * perform operations on them.
 */
RB.Dashboard = RB.DatagridPage.extend({
  rowObjectType: RB.ReviewRequest,

  /**
   * Close all selected review requests.
   *
   * This will keep track of all the successes and failures and report
   * them back to the caller once completed.
   *
   * Args:
   *     options (object):
   *         Options for the operation.
   *
   * Option Args:
   *     closeType (string):
   *         The close type to use (submitted or discarded).
   *
   *     onDone (function):
   *         A function to call when the operation is complete.
   */
  closeReviewRequests: function closeReviewRequests(options) {
    var reviewRequests = this.selection.clone();
    var successes = [];
    var failures = [];

    function closeNext() {
      if (reviewRequests.length === 0) {
        this.selection.reset();
        this.trigger('refresh');
        options.onDone(successes, failures);
        return;
      }

      var reviewRequest = reviewRequests.shift();
      reviewRequest.close({
        type: options.closeType,
        success: function success() {
          return successes.push(reviewRequest);
        },
        error: function error() {
          return failures.push(reviewRequest);
        },
        complete: closeNext.bind(this)
      });
    }

    closeNext.call(this);
  },

  /**
   * Update the visibility of the selected review requests.
   *
   * This expects to be passed in a properly bound function (either
   * addImmediately or removeImmediately) on either archivedReviewRequests or
   * mutedReviewRequests. This will keep track of all the successes and
   * failures, reporting them back to the caller.
   *
   * Args:
   *     visibilityFunc (function):
   *         The function to call for each review request.
   */
  updateVisibility: function updateVisibility(visibilityFunc) {
    var reviewRequests = this.selection.clone();
    var successes = [];
    var failures = [];

    function hideNext() {
      var _this = this;

      if (reviewRequests.length === 0) {
        this.selection.reset();
        this.trigger('refresh');
        return;
      }

      var reviewRequest = reviewRequests.shift();
      visibilityFunc(reviewRequest, {
        success: function success() {
          successes.push(reviewRequest);
          hideNext.call(_this);
        },
        error: function error() {
          failures.push(reviewRequest);
          hideNext.call(_this);
        }
      });
    }

    hideNext.call(this);
  }
});

//# sourceMappingURL=dashboardModel.js.map