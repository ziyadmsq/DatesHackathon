import React from 'react';

import { getColor } from 'utils/colors';

import {
  Card,
  CardBody,
  Col,
  Row,
} from 'reactstrap';

import Page from 'components/Page';
import Typography from 'components/Typography';
import { Line, Pie, Doughnut, Bar, Radar, Polar } from 'react-chartjs-2';


//TODO
const tree = {
  row: 2, col: 3,
  type: "Ajwah",
  yearPlanted: 2000,
  harvest: [{ date: "2019-9-10", amount: 70, quality: "HIGH" }, { date: "2019-9-20", amount: 60, quality: "MID" }, { date: "2019-9-25", amount: 70, quality: "HIGH" }],
  water: [{ date: "2019-9-24", amount: 20, }, { date: "2019-9-26", amount: 60, }, { date: "2019-9-29", amount: 50, },],
  pesticide: [{ date: "2019-9-10", amount: 0.5, }, { date: "2019-9-10", amount: 1.0, },],
  temp: generateData(20, 30),
  humidity: generateData(20, 80),
}

//dummydata
function generateData(min, delta) {
  let data = [];
  for (let i = 0; i < 500; i++) {
    let date = "2019-9-2" + Math.floor(i / 100);
    let value = Math.random() * delta + min;
    data.push({ date, value });
  }
  return data
}

function getWaterData(tree) {

  let labels = [];
  let values = [];

  tree.water.forEach(element => {
    labels.push(element.date);
    values.push(element.amount);
  });
  values.push(0);
  return {
    labels: labels,
    datasets: [
      {
        fill: false,
        label: "water usage",
        backgroundColor: getColor('primary'),
        borderColor: getColor('primary'),
        borderWidth: 1,
        data: values,
      },
    ],
  };
}

function getHarvestQuantityData(tree) {
  let labels = [];
  let values1 = [];

  tree.harvest.forEach(element => {
    labels.push(element.date);
    values1.push(element.amount);
  });
  values1.push(0);
  return {
    labels: labels,

    datasets: [{
      label: "Harvest Quantity",
      backgroundColor: getColor('success'),
      borderColor: getColor('success'),
      borderWidth: 1,
      data: values1,
    }],
  };
}

function getHarvestQualityData(tree) {
  let labels = [];
  let values1 = [];
  const qualities = ["LOW", "MID", "HIGH"];
  tree.harvest.forEach(element => {
    labels.push(element.date);
    values1.push(qualities.indexOf(element.quality) + 1);
  });
  values1.push(0);
  return {
    labels: labels,
    datasets: [{
      label: "Harvest Quality",
      backgroundColor: getColor('secondary'),
      borderColor: getColor('secondary'),
      borderWidth: 1,
      data: values1,
    }],
  };
}

function getPesticideData(tree) {
  let labels = [];
  let values1 = [];

  tree.pesticide.forEach(element => {
    labels.push(element.date);
    values1.push(element.amount);
  });
  values1.push(0);
  return {
    labels: labels,
    datasets: [{
      label: "Harvest Quality",
      backgroundColor: getColor('warning'),
      borderColor: getColor('warning'),
      borderWidth: 1,
      data: values1,
    }],
  };
}

function getTempData(arr, label) {

  let days = new Map();
  arr.forEach(entry => {
    if (!days.has(entry.date))
      days.set(entry.date, { min: 10000, max: -10000, sum: 0, count: 0 });
    let day = days.get(entry.date);
    days.set(entry.date, { date: entry.date, min: Math.min(day.min, entry.value), max: Math.max(day.max, entry.value), sum: day.sum + entry.value, count: day.count + 1 });
  });
  let labels = [];
  let min = [];
  let max = [];
  let avg = [];

  // console.log(days.values());

  for (var element of days.values()) {
    labels.push(element.date);
    min.push(element.min);
    max.push(element.max);
    avg.push(element.sum / element.count);
  }

  // forEach(element => {
  // });
  min.push(0);
  return {
    labels: labels,
    datasets: [{
      label: "Minimum " + label,
      backgroundColor: getColor('info'),
      borderColor: getColor('info'),
      borderWidth: 1,
      data: min,
      fill: false
    }, {
      label: "Average " + label,
      backgroundColor: getColor('success'),
      borderColor: getColor('success'),
      borderWidth: 1,
      data: avg,
      fill: false

    }, {
      label: "Maximum " + label,
      backgroundColor: getColor('danger'),
      borderColor: getColor('danger'),
      borderWidth: 1,
      data: max,
      fill: false

    }],
  };
}

const TreePage = () => {
  // console.log(new Date().getYear() + " hi ");

  return (
    <div className="container">
      <Col>
        <Card>
          <CardBody>
            <Typography type="display-4">
              {" Dates Palm " + tree.row + "," + tree.col} <br />
            </Typography>
            <Typography type="h5">
              Age : {new Date().getFullYear() - tree.yearPlanted}<br />
            </Typography>
            <hr />
            <Card>
              <Row>
                <Col xl={6} lg={12} md={12}>
                  <Card>
                    <Line data={getWaterData(tree)} />
                  </Card>
                </Col>
                <Col xl={6} lg={12} md={12}>
                  <Card>
                    <Bar data={getHarvestQuantityData(tree)} />
                  </Card>
                </Col>
                <Col xl={6} lg={12} md={12}>
                  <Card>
                    <Bar data={getHarvestQualityData(tree)} />
                  </Card>
                </Col>
                <Col xl={6} lg={12} md={12}>
                  <Card>
                    <Bar data={getPesticideData(tree)} />
                  </Card>
                </Col>
                <Col xl={6} lg={12} md={12}>
                  <Card>
                    <Line data={getTempData(tree.temp, "Tempreture")} />
                  </Card>
                </Col>
                <Col xl={6} lg={12} md={12}>
                  <Card>
                    <Line data={getTempData(tree.humidity, "Humidity")} />
                  </Card>
                </Col>
              </Row>
            </Card>
          </CardBody>
        </Card>
      </Col>

    </div>
  );
};

export default TreePage;
