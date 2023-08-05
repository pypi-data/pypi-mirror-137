// See templates/highlights/skeletal_frame.html for declaration of
// 1. highlightScope
// 2. footerContainer
// 3. highlightBtn
// 4. highlightInput

/**
 * This is the main highlighting function dependent on user selection of text.
 * - Whenever an "selection event" occurs in the `highlightable` text area, the container is hidden
 * - If the "selection event" results in a highlight selected, the container is made visible
 * - The `input` in a form is filled up with the highlight selected.
 * - The `input` is submitted when the user clicks on the button.
 * @returns
 */
document.onselectionchange = () => {
  footerContainer.setAttribute("hidden", true);
  highlightBtn.setAttribute("disabled", true);

  let textHighlighted = getSelectedText(highlightScope);
  if (!textHighlighted) return; // checks if highlight is allowed
  highlightInput.setAttribute("value", textHighlighted); // set input

  footerContainer.removeAttribute("hidden");
  highlightBtn.removeAttribute("disabled");
};

/**
 * Capture only if selected is within targeted
 * @param target the host container where text is permitted to be highlighted
 * @returns the string version of the DOM nodes highlighted
 */
function getSelectedText(target) {
  // make sure selected text is within the target
  let selection = nodesWithinTarget(target);
  if (!selection) return;

  // copy nodes to a holder which will then be converted to string
  let holder = document.createElement("div");
  for (let i = 0; i < selection.rangeCount; i++) {
    el = selection.getRangeAt(i).cloneContents();
    holder.append(el);
  }
  let textHighlighted = holder.innerHTML.toString();
  if (!textHighlighted || textHighlighted == "") return;

  return textHighlighted;
}

// return selectedNodes if allowed
const nodesWithinTarget = (targetNode) => {
  let selectedContent = document.getSelection();
  let targetAnchor = selectedContent.anchorNode;
  let allowed = targetNode.contains(targetAnchor);
  if (allowed) return selectedContent;
};
