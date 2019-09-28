import { AnnouncementCard, TodosCard } from 'components/Card';
import HorizontalAvatarList from 'components/HorizontalAvatarList';
import MapWithBubbles from 'components/MapWithBubbles';
import Page from 'components/Page';
import ProductMedia from 'components/ProductMedia';
import SupportTicket from 'components/SupportTicket';
import UserProgressTable from 'components/UserProgressTable';
import { IconWidget, NumberWidget } from 'components/Widget';
import { getStackLineChart, stackLineChartOptions } from 'demos/chartjs';
import { randomNum } from 'utils/demos';
import {
  avatarsData,
  chartjs,
  productsData,
  supportTicketsData,
  todosData,
  userProgressTableData,
} from 'demos/dashboardPage';
import React from 'react';
import { Bar, Line } from 'react-chartjs-2';
import {
  MdBubbleChart,
  MdInsertChart,
  MdPersonPin,
  MdPieChart,
  MdRateReview,
  MdShare,
  MdShowChart,
  MdThumbUp,
} from 'react-icons/md';
import InfiniteCalendar from 'react-infinite-calendar';
import {
  Badge,
  Button,
  Card,
  CardBody,
  CardDeck,
  CardGroup,
  CardHeader,
  CardTitle,
  Col,
  ListGroup,
  ListGroupItem,
  Row,
} from 'reactstrap';
import { getColor } from 'utils/colors';

const mS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];

const today = new Date();

class DashboardPage extends React.Component {
  componentWillMount() {
    // this is needed, because InfiniteCalendar forces window scroll
    // this.state = { data: { water: [0, 1], pesticide: [0, 1], harvest: [0], temp: 40, humidity: 50 } };
    // create a new XMLHttpRequest
    var xhr = new XMLHttpRequest()

    // get a callback when the server responds
    xhr.addEventListener('load', () => {
      let text = xhr.responseText
      text = text.replace(/\\/g, '');
      text = text.substring(1, text.length - 2);
      let tree1 = JSON.parse(text);

      console.log(tree1);

      this.setState({
        data: tree1,
      })
    })
    // open the request with the verb and the url
    xhr.open('GET', 'http://localhost:5000/api/recent/9nYhq5mcpaedhY9oM2L2jzmtKdx1')
    // send the request
    xhr.send()
  }

  getData() {
    let y1 = [];
    let y2 = [];
    if (this.state.data) {
      this.state.data.harvest.forEach(element => {
        if (y1.length < 12) y1.unshift(element);
        else y2.unshift(element);
      });
    }
    console.log(y1);
    console.log(y2);
    
    return {
      labels: mS,
      datasets: [
        {
          label: new Date().getFullYear(),
          backgroundColor: getColor('primary'),
          borderColor: getColor('primary'),
          borderWidth: 1,
          data: y1,
          fill:false
        },{
          label: new Date().getFullYear() - 1,
          backgroundColor: getColor('secondary'),
          borderColor: getColor('secondary'),
          borderWidth: 1,
          data: y2,
          fill:false

        }
      ],
    };
  }

  render() {
    const primaryColor = getColor('primary');
    const secondaryColor = getColor('secondary');
    if(!this.state)
      return (<p>loading...</p>);
    return (
      <Page
        className="DashboardPage"
        title="Dashboard"
        breadcrumbs={[{ name: 'Dashboard', active: true }]}
      >
        
        <Row>
          <Col lg={3} md={6} sm={6} xs={12}>
            <NumberWidget
              title="Total Harvest"
              subtitle="This year"
              number={this.state.data.harvest[0] / 1000 + " Tons"}
              color="secondary"
              progress={{
                value: 75,
                label: 'Average Quality',
              }}
            />
          </Col>

          <Col lg={3} md={6} sm={6} xs={12}>
            <NumberWidget
              title="Total Water Usage"
              subtitle="This month"
              number={this.state.data.water[0] / 1000 + " Tons"}
              color="secondary"
              progress={{
                value: Math.floor(this.state.data.water[0] / this.state.data.water[1] * 100),
                label: 'Last month',
              }}
            />
          </Col>

          <Col lg={3} md={6} sm={6} xs={12}>
            <NumberWidget
              title="Total Pesticide Usage"
              subtitle="This month"
              number={this.state.data.pesticide[0] / 1000 + " Kg"}
              color="secondary"
              progress={{
                value: Math.floor(this.state.data.pesticide[0] / this.state.data.pesticide[1] * 100),
                label: 'Last month',
              }}
            />
          </Col>

          <Col lg={3} md={6} sm={6} xs={12}>
            <NumberWidget
              title="Current Tempreture"
              subtitle="Today"
              number={this.state.data.degree}
              color="secondary"
              progress={{
                value: this.state.data.air_humidity,
                label: 'Air Humidity',
              }}
            />
          </Col>
        </Row>

        <Row>
          <Col lg="8" md="12" sm="12" xs="12">
            <Card>
              <CardHeader>Harvest compared to PREVIOUS year</CardHeader>
              <CardBody>
                <Line
                  data={this.getData()}
                  options={{
                    scales: {
                      xAxes: [
                        {
                          scaleLabel: {
                            display: true,
                            labelString: 'Month',
                          },
                        },
                      ],
                      yAxes: [
                        {
                          scaleLabel: {
                            display: true,
                            labelString: 'Value',
                          },
                        },
                      ],
                    },
                  }}
                />
              </CardBody>
              {/* <CardHeader>
                Total palms{' '}
                <small className="text-muted text-capitalize">This year</small>
              </CardHeader> */}
              {/* <CardBody>
                <Line data={chartjs.line.data} options={chartjs.line.options} />
              </CardBody> */}
            </Card>
          </Col>

          <Col lg="4" md="12" sm="12" xs="12">
            <Card>
              <CardHeader>Total Water/Pesticide Usage</CardHeader>
              <CardBody>
                <Bar data={chartjs.bar.data} options={chartjs.bar.options} />
              </CardBody>
            </Card>
            <hr />
            <AnnouncementCard
              color="gradient-secondary"
              header="Announcement"
              avatarSize={60}
              name="Jamy"
              date="1 hour ago"
              text="Lorem ipsum dolor sit amet,consectetuer edipiscing elit,sed diam nonummy euismod tinciduntut laoreet doloremagna"
              buttonProps={{
                children: 'show',
              }}
              style={{ height: 500 }}
            />

          </Col>
        </Row>



        <Row>
          <Col md="6" sm="12" xs="12">
            <Card>
              <CardHeader>Dates prices</CardHeader>
              <CardBody>
                {productsData.map(
                  ({ id, image, title, description, right }) => (
                    <ProductMedia
                      key={id}
                      image={image}
                      title={title}
                      description={description}
                      right={right}
                    />
                  ),
                )}
              </CardBody>
            </Card>
          </Col>

          <Col md="6" sm="12" xs="12">
            <Card>
              <CardHeader>workers</CardHeader>
              <CardBody>
                <UserProgressTable
                  headers={[
                    <MdPersonPin size={25} />,
                    'name',
                    'date',
                    'participation',
                    '%',
                  ]}
                  usersData={userProgressTableData}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>
      </Page>
    );
  }
}
export default DashboardPage;
