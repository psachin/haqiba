#!/usr/bin/env python
import os
import sys
import store

def populate_users():

    # Admin 
    os.system("python manage.py syncdb --noinput")
    os.system("python manage.py createsuperuser --username=admin --email=admin@example.com")

    for u in store.users:
    # Normal users
        u['USERNAME'] = add_user(u['USERNAME'], u['EMAIL'], u['PASSWORD'])
    
        add_user_profile(user=u['USERNAME'],
                         website=u['WEBSITE'],
                         picture=u['PHOTO'])

    user_list = User.objects.all()
    if user_list:
        print "Following user(s) created successfully."
        for i in user_list:
            print i.username

def populate_codes():
    
    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Show-paren",
        code="(show-paren-mode t)",
        description="Show matching parenthesis.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Battery",
        code="(display-battery-mode t)",
        description="Show battery status in mode line.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Sudo-edit",
        code="""
(defun sudo-edit (&optional arg)
  "Edit currently visited file as root.

With a prefix ARG prompt for a file to visit.
Will also prompt for a file to visit if current
buffer is not visiting a file."
  (interactive "P")
  (if (or arg (not buffer-file-name))
      (find-file (concat "/sudo:root@localhost:"
                         (ido-read-file-name "Find file(as root): ")))
    (find-alternate-file (concat "/sudo:root@localhost:" buffer-file-name))))
(global-set-key (kbd "C-x C-r") 'sudo-edit)""",
        description="Edit currently visited file as root. Key binding: C-x C-r",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Google",
        code="""
(defun google ()
  "Google the selected region if any, display a query prompt otherwise."
  (interactive)
  (browse-url
   (concat
    "http://www.google.com/search?ie=utf-8&oe=utf-8&q="
    (url-hexify-string (if mark-active
         (buffer-substring (region-beginning) (region-end))
       (read-string "Search Google: "))))))
(global-set-key (kbd "C-x g") 'google)""",
        description="Search Google using 'M-x google'. Keyboard shortcut C-x g. By Bozhidar Batsov. http://emacsredux.com/blog/2013/03/28/google/",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Youtube",
        code="""
(defun youtube ()
  "Search YouTube with a query or region if any."
  (interactive)
  (browse-url
   (concat
    "http://www.youtube.com/results?search_query="
    (url-hexify-string (if mark-active
                           (buffer-substring (region-beginning) (region-end))
                         (read-string "Search YouTube: "))))))
(global-set-key (kbd "C-x y") 'youtube)""",
        description="Search Youtube using 'M-x youtube'. Keyboard shortcut C-x y. By Bozhidar Batsov. http://emacsredux.com/blog/2013/08/26/search-youtube/",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="No-tool-menu-bar",
        code="""
(menu-bar-mode 0)
(tool-bar-mode 0)""",
        description="Hide tool-bar and menubar.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Server",
        code="""
(require 'server)
(unless (server-running-p)
  (server-start))""",
        description="Run emacs server so that emacs client can connect using 'emacsclient -nw' command.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Package",
        code="""
;; Marmalade repo
(require 'package)
(add-to-list 'package-archives
             '("marmalade" . "http://marmalade-repo.org/packages/") t)

;; Melpa repo
(add-to-list 'package-archives
	     '("melpa" . "http://melpa.milkbox.net/packages/") t)
(package-initialize)""",
        description="Add Marmalade and Melpa repos. Packages can be installed using 'M-x package-list-packages'.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Org-syntax-highlighting",
        code="""
;; Org-mode source syntax highlighting
;; http://praveen.kumar.in/2012/03/10/org-mode-latex-and-minted-syntax-highlighting/
;; Requires 'minted.sty' in PATH.
;; Download minted: http://www.ctan.org/tex-archive/macros/latex/contrib/minted
;; and run 'make' to generate 'minted.sty'.
(require 'org-latex)
(setq org-export-latex-listings 'minted)
(add-to-list 'org-export-latex-packages-alist '("" "minted"))
(setq org-src-fontify-natively t)

;; extending support for other languages so that we can execute them
;; in org mode.
;; http://www.johndcook.com/blog/2012/02/09/python-org-mode/
;; Add more extensions below.
(org-babel-do-load-languages
    'org-babel-load-languages '((python . t) 
				(R . t)
				(sh . t)
				(emacs-lisp . t)
				(clojure . t)
				(C . t)))""",
        description="Provide language specific syntax highlighting when converting org to PDF.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Inhibit-startup",
        code="""
(setq-default inhibit-startup-screen t)""",
        description="Inhibit startup-screen",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Word-wrap",
        code="""
;; turn on word wrap
(auto-fill-mode t)""",
        description="Turn on word wrap.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Hide-dot-files",
        code="""
;; Hide DOT files with M-o
(require 'dired-x)
(setq dired-omit-files "^\\...+$")

(add-hook 'dired-mode-hook
	  (lambda ()
	    ;; Set dired-x buffer-local variables here.  For example:
	    (dired-omit-mode 1)
	    ))""",
        description="Do not show dot(hidden) files in dired-mode.",
        screenshot="/screenshot/banner.png"
    )
    
    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Buffer-size",
        code="""
;; Show buffer size in mode-line.
(size-indication-mode t)""",
        description="Show buffer size in mode-line.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Column-number",
        code="""
;; Show column number in mode-line.
(column-number-mode t)""",
        description="Show column number in mode-line.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Elisp-doc",
        code="""
;; show elisp function docs in result bar
(add-hook 'emacs-lisp-mode-hook 'turn-on-eldoc-mode)
(add-hook 'lisp-interaction-mode-hook 'turn-on-eldoc-mode)
(add-hook 'ielm-mode-hook 'turn-on-eldoc-mode)""",
        description="Show elisp function documentation in result bar.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Word-count",
        code="""
;; Pluralize
(defun pluralize (word count &optional plural)
  "Pluralize the word."
  (if (= count 1)
      word
    (if (null plural)
	(concat word "s")
      plural)))

;; Count total number of words in current buffer
(defun count-words-buffer ()
  "Count total number of words in current buffer."
  (interactive)
  (let ((count 0))
    (save-excursion
      (goto-char (point-min))
      (while (< (point) (point-max))
	(forward-word 1)
	(setq count (1+ count)))
      (if (zerop count)
	  (message "buffer has no words.")
	(message "buffer approximately has %d %s." count 
		 (pluralize "word" count))))))
(global-set-key (kbd "C-x c") 'count-words-buffer)
""",
        description="Count total number of words in current buffer. Key binding: C-x c.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Terminal",
        code="""
;; terminal at your fingerprint
;; http://emacsredux.com/blog/page/2/
(defun visit-term-buffer ()
  "Create or visit a terminal buffer."
  (interactive)
  (if (not (get-buffer "*ansi-term*"))
      (progn
        (split-window-sensibly (selected-window))
        (other-window 1)
        (ansi-term (getenv "SHELL")))
    (switch-to-buffer-other-window "*ansi-term*")))
(global-set-key (kbd "C-c t") 'visit-term-buffer)""",
        description="Visit terminal buffer. Key binding: C-c t. From http://emacsredux.com/blog/page/2/",
        screenshot="/screenshot/banner.png"
    )    

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Percentage-buffer",
        code="""
(defun goto-percent (pct)
  "Go to place in a buffer expressed in percentage."
  (interactive "nPercent: ")
  (goto-char (/ (* (point-max) pct) 100)))
(global-set-key (kbd "C-x p") 'goto-percent)""",
        description="Go to place in a buffer expressed in percentage. Key binding: C-x p.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Org-mode-workflow-state",
        code="""
(setq org-todo-keywords
  '((sequence "TODO" "IN-PROGRESS" "WAITING" "DONE")))""",
        description="Add workflow state in org-mode.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Highlight-annotations",
        code="""
(defun font-lock-comment-annotations ()
  "Highlight a bunch of well known comment annotations.
This functions should be added to the hooks of major modes for
programming."
  (font-lock-add-keywords
   nil '(("\\<\\(FIX\\(ME\\)?\\|TODO\\|OPTIMIZE\\|HACK\\|REFACTOR\\):"
          1 font-lock-warning-face t))))
(add-hook 'prog-mode-hook 'font-lock-comment-annotations)""",
        description="Highlight comment annotations.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Global-indentation",
        code="""
(define-key global-map (kbd "RET") 'newline-and-indent)
(setq-default indent-tabs-mode t)""",
        description="http://doxdrum.wordpress.com/",
        screenshot="/screenshot/global-indentation.png"
    )

    add_code_template(
        user_id=store.user1['USERNAME'].id,
        name="Viooz",
        code="""
(defun viooz ()
  "Search movie on Viooz.co with selected region if any, display a query prompt otherwise."
  (interactive)
  (browse-url
   (concat
    "http://viooz.co/search?q="
    (url-hexify-string (if mark-active
			   (buffer-substring (region-beginning) (region-end))
			 (read-string "Search Viooz.co: "))) "&s=t")))
(global-set-key (kbd "C-c v") 'viooz)""",
        description="Search movie on Viooz.co from Emacs. Based on Bozhidar Batsov's \
        'Google'. Key binding 'C-c v' ",
        screenshot="/screenshot/viooz.png"
    )

    add_code_template(
        user_id=store.user2['USERNAME'].id,
        name="Delete-current-buffer-file",
        code="""
(defun delete-current-buffer-file ()
  "Removes file connected to current buffer and kills buffer."
  (interactive)
  (let ((filename (buffer-file-name))
	(buffer (current-buffer))
	(name (buffer-name)))
    (if (not (and filename (file-exists-p filename)))
	(ido-kill-buffer)
      (when (yes-or-no-p "Are you sure you want to remove this file? ")
	(delete-file filename)
	(kill-buffer buffer)
	(message "File '%s' successfully removed" filename)))))
(global-set-key (kbd "C-x C-k") 'delete-current-buffer-file)""",
        description="http://whattheemacsd.com/",
        screenshot="/screenshot/delete_buffer-file.png",
        download_count=10,
    )

    print "---------- Codes ------------"
    for c in CodeTemplate.objects.all():
        print c.name

        # Populate Codes ends here.
        
    epc = add_package(user_id=store.user1['USERNAME'].id,
                      name="emacs-epc",
                      description="emacs-epc, https://github.com/kiwanami/emacs-epc",
                      tarFile="deps/emacs-epc.tar",
                      config="",
                      screenshot=None)
    epc.save()

    deferred = add_package(user_id=store.user1['USERNAME'].id,
                           name="emacs-deferred",
                           description="emacs-deferred, https://github.com/kiwanami/emacs-deferred",
                           tarFile="deps/emacs-deferred.tar",
                           config="",
                           screenshot=None)
    deferred.save()
    
    ctable = add_package(user_id=store.user1['USERNAME'].id,
                         name="emacs-ctable",
                         description="emacs-ctable, https://github.com/kiwanami/emacs-ctable",
                         tarFile="deps/emacs-ctable.tar",
                         config="",
                         screenshot=None)
    ctable.save()

    jedi = add_package(user_id=store.user1['USERNAME'].id,
                       name="emacs-jedi",
                       description="emacs-jedi, https://github.com/tkf/emacs-jedi",
                       tarFile="deps/emacs-jedi.tar",
                       config="",
                       screenshot=None)
    jedi.save()

    yas = add_package(user_id=store.user1['USERNAME'].id,
                      name="yasnippet",
                      description="Template system for Emacs. https://github.com/capitaomorte/yasnippet",
                      tarFile="deps/yasnippet.tar",
                      config="""(yas-global-mode 1)""",
                      screenshot="screenshot/banner.png")
    yas.save()

    rainbow_delimiter = add_package(user_id=store.user1['USERNAME'].id,
                                    name="rainbow-delimiter",
                                    description="highlights parentheses, brackets, and braces according to their depth. Each successive level is highlighted in a different color. https://github.com/jlr/rainbow-delimiters",
                                    tarFile="deps/rainbow-delimiters.tar",
                                    config="""(add-hook 'clojure-mode-hook 'rainbow-delimiters-mode)
(add-hook 'prog-mode-hook 'rainbow-delimiters-mode)
(global-rainbow-delimiters-mode)""",
                                    screenshot="screenshot/rainbow_delimiter.png",
    )
    rainbow_delimiter.save()

    autopair = add_package(user_id=store.user1['USERNAME'].id,
                           name="autopair",
                           description="Automagically pair braces and quotes in emacs like TextMate. https://github.com/capitaomorte/autopair",
                           tarFile="deps/autopair.tar",
                           config="""(autopair-global-mode)""",
                           screenshot="screenshot/autopair.png")
    autopair.save()
    
    print "---------- Packages ------------"
    for p in Dependency.objects.all():
        print p.name

    # Populate Packages ends here.
    python = add_bundle(user_id=store.user1['USERNAME'].id,
                        name="Python",
                        description="Python bundle. Includes emacs-epc, emacs-deferred, emacs-ctables & emacs-jedi.",
                        config="""(add-hook 'python-mode-hook 'jedi:setup)
(add-hook 'python-mode-hook 'jedi:ac-setup)
(setq jedi:setup-keys t)                      ; optional
(setq jedi:complete-on-dot t)                 ; optional""",
               screenshot="/screenshot/banner.png",)

    python.save()
    python.dep.add(epc, deferred, ctable, jedi)

    parentheses = add_bundle(user_id=store.user1['USERNAME'].id,
                             name="Parentheses",
                             description="Parentheses. Includes autopair & rainbow-delimiter.",
                             config="",
                             screenshot="/screenshot/banner.png",)

    parentheses.save()
    parentheses.dep.add(rainbow_delimiter, autopair)
    
    print "---------- Bundle ------------"
    for b in BundleTemplate.objects.all():
        print "........"
        print b.name
        print "Depends on: "
        for i in b.dep.all():
            print "\t %s" % i
    
def add_user(username, email, password):
    u = User.objects.create_user(username=username, email=email, 
                                          password=password)
    return u

def add_user_profile(user, website, picture):
    up = UserProfile(user=user, website=website, picture=picture)
    up.save()

def add_code_template(user_id, name, code, description, screenshot=None, 
                      download_count=0):
    c = CodeTemplate(user_id=user_id, name=name, code=code, 
                     description=description, screenshot=screenshot, 
                     download_count=download_count)
    c.save()

def add_package(user_id, name, description, tarFile, config, screenshot, download_count=0):
    p = Dependency(user_id=user_id, name=name, description=description,
                   tarFile=tarFile, config=config,
                   download_count=download_count, screenshot=screenshot)
    return p

def add_bundle(user_id, name, description, config, screenshot=None,
               download_count=0):
    b = BundleTemplate(user_id=user_id, name=name, description=description,
                       config=config, screenshot=screenshot,
                       download_count=download_count)
    return b
    
# Start execution here!
if __name__ == '__main__':
    print "Starting Haqiba population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'haqiba.settings')
    from emacshaqiba.models import CodeTemplate, UserProfile, Dependency
    from emacshaqiba.models import BundleTemplate
    from django.contrib.auth.models import User

    if os.path.exists('haqiba.db'):
        os.system("rm haqiba.db")

    populate_users()
    populate_codes()
