function formatTime(inputTime) {
  const date = new Date(inputTime);
  const now = new Date();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const ampm = hours >= 12 ? "pm" : "am";
  const formattedHours = hours % 12 || 12;

  if (date.toDateString() === now.toDateString()) {
    return `today ${formattedHours}:${minutes
      .toString()
      .padStart(2, "0")}${ampm}`;
  } else {
    return `${date.toDateString()} ${formattedHours}:${minutes
      .toString()
      .padStart(2, "0")}${ampm}`;
  }
}

export default formatTime;
