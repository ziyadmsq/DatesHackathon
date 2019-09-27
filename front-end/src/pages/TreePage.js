import React from 'react';

import { getColor } from 'utils/colors';

import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Col,
  Form,
  FormFeedback,
  FormGroup,
  FormText,
  Input,
  Label,
  Row,
} from 'reactstrap';

import Page from 'components/Page';
import Typography from 'components/Typography';
import { Line, Pie, Doughnut, Bar, Radar, Polar } from 'react-chartjs-2';

import { NumberWidget, IconWidget } from 'components/Widget';

import { iconWidgetsData, numberWidgetsData } from 'demos/widgetPage';

//TODO
const tree = {
  row: 2, col: 3,
  type: "خلاص",
  yearPlanted: 2000,
  harvest: [{ date: "2019-9-10", amount: 70, quality: "HIGH" }, { date: "2019-9-20", amount: 60, quality: "MID" }, { date: "2019-9-25", amount: 70, quality: "HIGH" }],
  water: [{ date: "2019-9-24", amount: 20, }, { date: "2019-9-26", amount: 60, }],
  pesticide: [[{ date: { year: 2019, month: 9, day: 24, }, amount: 1.0, }, { date: { year: 2019, month: 9, day: 26, }, amount: 1.0, },],],
  temp: [],
  humidity: [],
}

function getData(tree) {

  let labels = [];
  let values = [];

  tree.water.forEach(element => {
    labels.push(element.date);
    values.push(element.amount);
  });

  return {
    labels: labels,
    datasets: [
      {
        label: 'كمية المياه (لتر(',
        backgroundColor: getColor('primary'),
        borderColor: getColor('primary'),
        borderWidth: 1,
        data: values,
      },
    ],
  };
}

const TreePage = () => {
  // console.log(new Date().getYear() + " hi ");

  return (
    <div className="container">
      <Col xl={6} lg={12} md={12}>
        <Card>
          <CardBody>
            <Typography type="display-4">
              {" النخلة " + tree.row + "," + tree.col} <br />
            </Typography>
            <Typography type="h5">
              عمر النخلة : {new Date().getFullYear() - tree.yearPlanted}<br />
            </Typography>
            <Bar data={getData(tree)} />
          </CardBody>
        </Card>
      </Col>

    </div>
  );
};

export default TreePage;
