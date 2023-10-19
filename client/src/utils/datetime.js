const monthNames = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const datetime = (timestamp) => {
  let dt = timestamp.split(" ")[0];
  let dtmm = dt.split("/")[0];
  let dtdd = dt.split("/")[1];
  let dtyy = dt.split("/")[2];
  let time = timestamp.split(" ")[1];
  let timehh = time.split(":")[0];
  let timemm = time.split(":")[1];
  let month = monthNames[dtmm - 1];

  return { month, dtmm, dtdd, dtyy, timehh, timemm };
};

export default datetime;
