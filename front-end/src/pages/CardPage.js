import bg11Image from 'assets/img/bg/background_1920-11.jpg';
import bg18Image from 'assets/img/bg/background_1920-18.jpg';
import bg1Image from 'assets/img/bg/palm_tree.png';
import bg3Image from 'assets/img/bg/background_640-3.jpg';
import user1Image from 'assets/img/users/100_1.jpg';
import { UserCard } from 'components/Card';
import Page from 'components/Page';
import { bgCards, gradientCards, overlayCards } from 'demos/cardPage';
import { getStackLineChart, stackLineChartOptions } from 'demos/chartjs';
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Button,
  Card,
  CardBody,
  CardImg,
  CardImgOverlay,
  CardLink,
  CardText,
  CardTitle,
  Col,
  ListGroup,
  ListGroupItem,
  Row,
} from 'reactstrap';

function createnakh() {
  console.log("HI find me!")
  let data = [];
  for (let i = 1; i <= 100; i++) {
    data.push(<Col md={2} sm={2} xs={3} className="mb-3">
      <a href="http://localhost:3000/login">
        <Card className="flex-row">
          <div style={{ float: "none", margin: "0 auto" }} >
            <img
              className="card-img"
              src={bg1Image}
              style={{ width: 40, height: 50, marginLeft: "25%", marginTop: "50%" }}
            />
            <CardBody>
              <CardTitle >نخلة رقم {i} </CardTitle>
            </CardBody>
          </div>
        </Card>
      </a>

    </Col>);

  }
  return <Row classID="Rows">{data}</Row>

}

const CardPage = () => {
  return (
    <Page title="Cards" breadcrumbs={[{ name: 'cards', active: true }]}>

      {createnakh()}



    </Page>
  );
};

export default CardPage;
