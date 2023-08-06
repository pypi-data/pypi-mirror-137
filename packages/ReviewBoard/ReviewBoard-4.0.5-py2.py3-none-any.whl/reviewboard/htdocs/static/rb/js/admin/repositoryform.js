"use strict";

(function () {
  var prevTypes = {};
  var origRepoTypes = [];
  var powerPackTemplate = "<h3>".concat(gettext("Power Pack Required"), "</h3>\n<p>\n").concat(gettext("<span class=\"power-pack-advert-hosting-type\"></span> support is available with <a href=\"https://www.reviewboard.org/powerpack/\">Power Pack</a>, an extension which also offers powerful reports, document review, and more."), "\n</p>");
  var gerritPluginRequiredTemplate = "<h3>\n".concat(gettext("Plugin Required"), "\n</h3>\n<p>\n").concat(interpolate(gettext("The <code>gerrit-reviewboard</code> plugin is required for Gerrit integration. See the <a href=\"%s\" target=\"_blank\">instructions</a> for installing the plugin on your server."), [MANUAL_URL + 'admin/configuration/repositories/gerrit/']), "\n</p>");

  function updatePlanEl($row, $plan, serviceType, isFake) {
    var planTypes = HOSTING_SERVICES[serviceType].plans;
    var selectedPlan = $plan.val();
    $plan.empty();

    if (planTypes.length === 1 || isFake) {
      $row.hide();
    } else {
      for (var i = 0; i < planTypes.length; i++) {
        var planType = planTypes[i];
        var opt = $('<option/>').val(planType.type).text(planType.label).appendTo($plan);

        if (planType.type === selectedPlan) {
          opt.prop('selected', true);
        }
      }

      $row.show();
    }

    $plan.triggerHandler('change');
  }

  function updateHostingForm($hostingType, formPrefix, $plan, $forms) {
    var formID = "#".concat(formPrefix, "-").concat($hostingType.val(), "-").concat($plan.val() || 'default');
    $forms.hide();
    $(formID).show();
  }

  function updateRepositoryType() {
    var hostingType = $('#id_hosting_type').val();
    var newRepoTypes = hostingType === 'custom' ? [] : HOSTING_SERVICES[hostingType].scmtools;
    var $repoTypes = $('#id_tool');
    var currentRepoType = $repoTypes.val();
    $repoTypes.empty();
    origRepoTypes.forEach(function (repoType) {
      if (newRepoTypes.length === 0 || newRepoTypes.indexOf(repoType.text) !== -1 || newRepoTypes.indexOf(repoType.value) !== -1) {
        $('<option/>').text(repoType.text).val(repoType.value).appendTo($repoTypes);

        if (repoType.value === currentRepoType) {
          $repoTypes.val(currentRepoType);
        }
      }
    });
    $repoTypes.triggerHandler('change');
  }

  function updateAccountList() {
    var hostingType = $('#id_hosting_type').val();
    var $hostingAccount = $('#id_hosting_account');
    var $authForm = $('#hosting-auth-form-' + hostingType);
    var hostingInfo = HOSTING_SERVICES[hostingType];
    var accounts = hostingInfo.accounts;
    var selectedAccount = parseInt($hostingAccount.val(), 10);
    var foundSelected = false;
    /* Rebuild the list of accounts. */

    $hostingAccount.find('option[value!=""]').remove();

    if (hostingInfo.needs_two_factor_auth_code || $authForm.find('.errorlist').length > 0) {
      /*
       * The first one will be selected automatically, which
       * we want. Don't select any below.
       */
      foundSelected = true;
    }

    accounts.forEach(function (account) {
      var text = account.username;

      if (account.hosting_url) {
        text += " (".concat(account.hosting_url, ")");
      }

      var $opt = $('<option/>').val(account.pk).text(text).data('account', account).appendTo($hostingAccount);

      if (account.pk === selectedAccount || !foundSelected) {
        $opt.prop('selected', true);
        foundSelected = true;
        $hostingAccount.triggerHandler('change');
      }
    });
  }

  $(document).ready(function () {
    var $hostingType = $('#id_hosting_type');
    var $hostingAuthForms = $('.hosting-auth-form');
    var $hostingRepoForms = $('.hosting-repo-form');
    var $hostingAccount = $('#id_hosting_account');
    var $hostingAccountRow = $('#row-hosting_account');
    var $hostingAccountRelink = $('<p/>').text(gettext("The authentication requirements for this account have changed. You will need to re-authenticate.")).addClass('errornote').hide().appendTo($hostingAccountRow);
    var $scmtoolAuthForms = $('.scmtool-auth-form');
    var $scmtoolRepoForms = $('.scmtool-repo-form');
    var $associateSshKeyFieldset = $('#row-associate_ssh_key').parents('fieldset');
    var $associateSshKey = $('#id_associate_ssh_key');
    var associateSshKeyDisabled = $associateSshKey.prop('disabled');
    var $bugTrackerUseHosting = $('#id_bug_tracker_use_hosting');
    var $bugTrackerUseHostingRow = $('#row-bug_tracker_use_hosting');
    var $bugTrackerType = $('#id_bug_tracker_type');
    var $bugTrackerHostingURLRow = $('#row-bug_tracker_hosting_url');
    var $bugTrackerTypeRow = $('#row-bug_tracker_type');
    var $bugTrackerPlan = $('#id_bug_tracker_plan');
    var $bugTrackerPlanRow = $('#row-bug_tracker_plan');
    var $bugTrackerURLRow = $('#row-bug_tracker');
    var $bugTrackerUsernameRow = $('#row-bug_tracker_hosting_account_username');
    var $repoPlanRow = $('#row-repository_plan');
    var $repoPlan = $('#id_repository_plan');
    var $publicAccess = $('#id_public');
    var $tool = $('#id_tool');
    var $toolRow = $('#row-tool');
    var $showSshKey = $('#show-ssh-key-link');
    var $publicKeyPopup = $('#ssh-public-key-popup');
    var $bugTrackerForms = $('.bug-tracker-form');
    var $submitButtons = $('input[type="submit"]');
    var $editHostingCredentials = $('#repo-edit-hosting-credentials');
    var $editHostingCredentialsLabel = $('#repo-edit-hosting-credentials-label');
    var $forceAuth = $('#id_force_authorize');
    var $powerPackAdvert = $('<div class="powerpack-advert" />').html(powerPackTemplate).hide().appendTo($hostingType.closest('fieldset'));
    var $gerritPluginInfo = $('<div class="gerrit-plugin-advert" />').html(gerritPluginRequiredTemplate).hide().appendTo($('#row-hosting_type'));
    prevTypes.bug_tracker_type = 'none';
    prevTypes.hosting_type = 'custom';
    prevTypes.tool = 'none';
    $tool.find('option').each(function (i, el) {
      var $repoType = $(el);
      origRepoTypes.push({
        value: $repoType.val(),
        text: $repoType.text()
      });
    });
    $bugTrackerUseHosting.change(function () {
      if (this.checked) {
        $bugTrackerTypeRow.hide();
        $bugTrackerPlanRow.hide();
        $bugTrackerUsernameRow.hide();
        $bugTrackerURLRow.hide();
        $bugTrackerForms.hide();
      } else {
        $bugTrackerTypeRow.show();
        $bugTrackerType.triggerHandler('change');
      }
    }).triggerHandler('change');
    $repoPlan.change(function () {
      return updateHostingForm($hostingType, 'repo-form-hosting', $repoPlan, $hostingRepoForms);
    });
    $bugTrackerPlan.change(function () {
      var plan = $bugTrackerPlan.val() || 'default';
      var bugTrackerType = $bugTrackerType.val();
      var planInfo = HOSTING_SERVICES[bugTrackerType].planInfo[plan];
      updateHostingForm($bugTrackerType, 'bug-tracker-form-hosting', $bugTrackerPlan, $bugTrackerForms);
      $bugTrackerUsernameRow.setVisible(planInfo.bug_tracker_requires_username);
    });
    $hostingType.change(function () {
      var hostingType = $hostingType.val();
      var isCustom = hostingType === 'custom';
      var isFake = !isCustom && HOSTING_SERVICES[hostingType].fake === true;
      updateRepositoryType();
      $gerritPluginInfo.toggle(hostingType === 'gerrit');

      if (isCustom) {
        $repoPlanRow.hide();
      } else {
        $scmtoolAuthForms.hide();
        $scmtoolRepoForms.hide();
        updatePlanEl($repoPlanRow, $repoPlan, hostingType, isFake);
      }

      $repoPlan.triggerHandler('change');

      if (isCustom || isFake || !HOSTING_SERVICES[hostingType].supports_bug_trackers) {
        $bugTrackerUseHostingRow.hide();
        $bugTrackerUseHosting.prop({
          disabled: true,
          checked: false
        }).triggerHandler('change');
      } else {
        $bugTrackerUseHosting.prop('disabled', false);
        $bugTrackerUseHostingRow.show();
      }

      if (isCustom || !HOSTING_SERVICES[hostingType].supports_ssh_key_association) {
        $associateSshKeyFieldset.hide();
        $associateSshKey.prop({
          disabled: true,
          checked: false
        });
      } else {
        /*
         * Always use the original state of the checkbox (i.e. the
         * state on page load)
         */
        $associateSshKey.prop('disabled', associateSshKeyDisabled);
        $associateSshKeyFieldset.show();
      }

      if (isFake) {
        $powerPackAdvert.find('.power-pack-advert-hosting-type').text($hostingType.find(':selected').text());
      }

      $hostingAccountRow.setVisible(!isFake);
      $toolRow.setVisible(!isFake);
      $powerPackAdvert.setVisible(isFake);
      $submitButtons.prop('disabled', isFake);

      if (!isCustom) {
        updateAccountList();
      }
    }).triggerHandler('change');
    $([$hostingType[0], $hostingAccount[0]]).change(function () {
      $hostingAuthForms.hide();
      $hostingAccountRelink.hide();
      $editHostingCredentials.hide().val(gettext("Edit credentials"));
      $forceAuth.val('false');
      var hostingType = $hostingType.val();

      if (hostingType === 'custom') {
        $hostingAccountRow.hide();
      } else {
        var hostingInfo = HOSTING_SERVICES[hostingType];

        if (hostingInfo.fake !== true) {
          $hostingAccountRow.show();
          var $authForm = $('#hosting-auth-form-' + hostingType);
          /*
           * Hide any fields required for 2FA unless explicitly
           * needed.
           */

          $authForm.find('[data-required-for-2fa]').closest('.form-row').setVisible(hostingInfo.needs_two_factor_auth_code);

          if ($hostingAccount.val() === '') {
            /* Present fields for linking a new account. */
            $authForm.show();
          } else if (hostingInfo.needs_two_factor_auth_code) {
            /*
             * The user needs to enter a 2FA code. We need to
             * show the auth form, and ensure we will be forcing
             * authentication.
             */
            $forceAuth.val('true');
            $authForm.show();
          } else {
            /* An existing linked account has been selected. */
            var selectedIndex = $hostingAccount[0].selectedIndex;
            var $selectedOption = $($hostingAccount[0].options[selectedIndex]);
            var account = $selectedOption.data('account');

            if (account.is_authorized && $authForm.find('.errorlist').length === 0) {
              $editHostingCredentials.show();
            } else {
              $authForm.show();
              $hostingAccountRelink.show();
            }
          }
        }
      }
    }).triggerHandler('change');
    $tool.change(function () {
      if ($hostingType.val() === 'custom') {
        var scmtoolID = $('#id_tool').val(),
            $authForm = $('#auth-form-scm-' + scmtoolID),
            $repoForm = $('#repo-form-scm-' + scmtoolID);
        $scmtoolAuthForms.hide();
        $scmtoolRepoForms.hide();
        $authForm.show();
        $repoForm.show();
      }
    }).triggerHandler('change');
    $bugTrackerType.change(function () {
      $bugTrackerForms.hide();
      var bugTrackerType = $bugTrackerType.val();

      if (bugTrackerType === 'custom' || bugTrackerType === 'none') {
        $bugTrackerHostingURLRow.hide();
        $bugTrackerPlanRow.hide();
        $bugTrackerUsernameRow.hide();
      }

      if (bugTrackerType === 'custom') {
        $bugTrackerURLRow.show();
      } else if (bugTrackerType === 'none') {
        $bugTrackerURLRow.hide();
      } else {
        $bugTrackerURLRow.hide();
        updatePlanEl($bugTrackerPlanRow, $bugTrackerPlan, bugTrackerType, false);
        $bugTrackerHostingURLRow.setVisible(HOSTING_SERVICES[bugTrackerType].self_hosted);
      }
    }).triggerHandler('change');
    $publicAccess.change(function () {
      var visible = !this.checked;
      $('#row-users').setVisible(visible);
      $('#row-review_groups').setVisible(visible);
    }).triggerHandler('change');
    $showSshKey.on('click', function () {
      if ($publicKeyPopup.is(':visible')) {
        $showSshKey.text(gettext("Show your SSH public key"));
        $publicKeyPopup.hide();
      } else {
        $showSshKey.text(gettext("Hide your SSH public key"));
        $publicKeyPopup.show();
      }

      return false;
    });
    $editHostingCredentials.click(function () {
      var $authForm = $('#hosting-auth-form-' + $hostingType.val());

      if ($forceAuth.val() === 'true') {
        $editHostingCredentialsLabel.text(gettext("Edit credentials"));
        $authForm.hide();
        $forceAuth.val('false');
      } else {
        $editHostingCredentialsLabel.text(gettext("Cancel editing credentials"));
        $authForm = $('#hosting-auth-form-' + $hostingType.val()).show();
        $authForm.show();
        $forceAuth.val('true');
      }

      return false;
    });
  });
})();

//# sourceMappingURL=repositoryform.js.map