#!/usr/bin/env python
import os
import sys
import store

def populate():

    store.USERNAME = add_user(store.USERNAME, store.EMAIL, store.PASSWORD)
    
    add_user_profile(user=store.USERNAME, 
                     website=store.WEBSITE,
                     picture=store.PHOTO)
    
    add_code_template(
        user_id=store.USERNAME.id,
        name="Show-paren",
        code="(show-paren-mode t)",
        description="Show matching parenthesis.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.USERNAME.id,
        name="Battery",
        code="(display-battery-mode t)",
        description="Show battery status in mode line.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.USERNAME.id,
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
        description="Edit currently visited file as root. Keybinding: C-x C-r",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.USERNAME.id,
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
        user_id=store.USERNAME.id,
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
        user_id=store.USERNAME.id,
        name="No-tool-menu-bar",
        code="""
(menu-bar-mode 0)
(tool-bar-mode 0)""",
        description="Hide tool-bar and menubar.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.USERNAME.id,
        name="Server",
        code="""
(require 'server)
(unless (server-running-p)
  (server-start))""",
        description="Run emacs server so that emacs client can connect using 'emacsclient -nw' command.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.USERNAME.id,
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
        user_id=store.USERNAME.id,
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
        description="Provide language specific ayntax highlighting when converting org to PDF.",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.USERNAME.id,
        name="Inhibit-startup",
        code="""
(setq-default inhibit-startup-screen t)""",
        description="Inhibit startup-screen",
        screenshot='screenshot/banner.png'
    )

    add_code_template(
        user_id=store.USERNAME.id,
        name="Word-wrap",
        code="""
;; turn on word wrap
(auto-fill-mode t)""",
        description="Turn on word wrap.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.USERNAME.id,
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
        user_id=store.USERNAME.id,
        name="Buffer-size",
        code="""
;; Show buffer size in mode-line.
(size-indication-mode t)""",
        description="Show buffer size in mode-line.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.USERNAME.id,
        name="Column-number",
        code="""
;; Show column number in mode-line.
(column-number-mode t)""",
        description="Show column number in mode-line.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.USERNAME.id,
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
        user_id=store.USERNAME.id,
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
        description="Count total number of words in current buffer. Keybinding: C-x c.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.USERNAME.id,
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
        description="Visit terminal buffer. Keybinding: C-c t. From http://emacsredux.com/blog/page/2/",
        screenshot="/screenshot/banner.png"
    )    

    add_code_template(
        user_id=store.USERNAME.id,
        name="Percentage-buffer",
        code="""
(defun goto-percent (pct)
  "Go to place in a buffer expressed in percentage."
  (interactive "nPercent: ")
  (goto-char (/ (* (point-max) pct) 100)))
(global-set-key (kbd "C-x p") 'goto-percent)""",
        description="Go to place in a buffer expressed in percentage. Keybinding: C-x p.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.USERNAME.id,
        name="Org-mode-workflow-state",
        code="""
(setq org-todo-keywords
  '((sequence "TODO" "IN-PROGRESS" "WAITING" "DONE")))""",
        description="Add workflow state in org-mode.",
        screenshot="/screenshot/banner.png"
    )

    add_code_template(
        user_id=store.USERNAME.id,
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

    for c in CodeTemplate.objects.all():
        print c.name

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

# Start execution here!
if __name__ == '__main__':
    print "Starting Haqiba population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'haqiba.settings')
    from emacshaqiba.models import CodeTemplate, UserProfile
    from django.contrib.auth.models import User
    os.system("rm haqiba.db")
    os.system("python manage.py syncdb --noinput")
    os.system("python manage.py createsuperuser --username=admin --email=admin@example.com")
    populate()
