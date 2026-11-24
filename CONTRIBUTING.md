# Contributing & Project Management
- [Reporting Bugs & Requesting Features](#reporting-bugs--requesting-features)
- [How Work Is Tracked](#how-work-is-tracked)
- [Pull Requests & Branching](#pull-requests--branching)

## Reporting Bugs & Requesting Features

> Issues are this project tracks anything broken, missing, or worth improving, so it can be prioritized on the Project board (see [How Work is Tracked](#how-work-is-tracked) below).
> 
> Before creating an issue, please check existing issues to see if the problem has already been reported.

**Labels:**

Every issue should get one at least one label. Some examples of labels for this project include:
- **`bug`** — something is broken or not working as intended
- **`feature`** — something new that doesn't exist yet
- **`enhancement`** — something that already works, but could be extended or made better
- **`usability`** — something that works correctly, but is confusing, awkward, or unclear to actually use

**Writing a Good Issue Title:**

A title should be concise, but specific enough that someone scanning the issue list knows what it's about without opening it.

- **Too vague:** "Roster bug"
- **Better:** "Roster page crashes when adding a player with no position selected" 

**Which Template do I Use?**
- Reporting something broken? Use the **Bug Report** template.
- Requesting something new, an improvement, or a usability fix? Use the **Feature Request** template and use the label(s) that matches the request.

## How Work Is Tracked

Work is tracked on the [Lady Devils Hub Roadmap](https://github.com/rakiranelson/lady-devils-hub/projects) GitHub Project board.

- Issues move through a status columns **Backlog -> Ready -> In Progress -> etc.** as work progresses. An issue in **Ready** is ready to be picked up.
- Each issue also has a **Priority** and **Effort** field attached to it. Use these to decide which **Ready** issue to take on.
    > The **Priority** and **Effort** views group issues by each of these fields, making it easy to compare options before starting something new. You should update these views for any new issues.

## Pull Requests & Branching

### Why are branches required for this project?
> Every push to `main` triggers the CI/CD pipeline (tests, build, and a deploy step that waits for manual approval). While manual approval means unfinished code won't actually go live on its own, pushing directly to `main` for every intermediate change still runs the pipeline unnecessarily each time and generates an approval request for code that isn't actually ready.

**Branch naming:** 

Name branches after the label of the issue they address, followed by a short description. For example:

```
bug/roster-player-crash
feature/rsvp-backend
enhancement/announcement-filtering
usability/unclear-error-messages
```

**Creating a branch:**
```bash
git checkout -b branch-name
git push --set-upstream origin branch-name
```

**Working on someone else's branch:**
```bash
git fetch origin
git checkout branch-name
```

**Opening a pull request:** 
- Include `Closes #<issue number>` in the PR description to automatically close the related issue when it's merged.

**Other notes:**
- Pull before you push, to avoid conflicts with changes already merged into the branch.
