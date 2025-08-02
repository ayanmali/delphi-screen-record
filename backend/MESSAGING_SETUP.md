# Candidate Invitation Messaging System

This document describes the messaging system for candidate invitations between the Java backend and Python service.

## Overview

When a candidate is invited to an assessment in the Java backend, a message is published to a RabbitMQ queue. The Python service consumes these messages and updates its database accordingly.

## Architecture

1. **Java Backend (Publisher)**: Publishes candidate invitation messages to RabbitMQ
2. **RabbitMQ**: Message broker that handles message routing
3. **Python Service (Consumer)**: Consumes messages and updates the database

## Message Flow

1. User invites a candidate to an assessment in the Java backend
2. `AssessmentService.addCandidateFromNew()` or `addCandidateFromExisting()` is called
3. `CandidateInvitationPublisher` publishes a message to RabbitMQ
4. Python consumer receives the message and updates its database

## Setup

### 1. Start RabbitMQ

```bash
# Using Docker Compose (recommended)
docker-compose up rabbitmq

# Or using Docker directly
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### 2. Configure Environment Variables

Add the following to your `.env` file:

```env
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

### 3. Install Python Dependencies

```bash
cd backend
uv sync
```

### 4. Run the Consumer

```bash
# Option 1: Run directly
python run_consumer.py

# Option 2: Run with logging
python -u run_consumer.py 2>&1 | tee consumer.log
```

## Message Structure

The candidate invitation message contains:

```json
{
  "assessment_id": 123,
  "assessment_name": "Frontend Developer Assessment",
  "assessment_description": "Test frontend skills",
  "assessment_type": "CODING",
  "assessment_start_date": "2024-01-15T10:00:00",
  "assessment_end_date": "2024-01-15T12:00:00",
  "assessment_duration": 120,
  "candidate": {
    "id": 456,
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com"
  },
  "user_id": 789,
  "user_email": "employer@company.com",
  "invitation_date": "2024-01-10T14:30:00",
  "invitation_id": "uuid-string"
}
```

## Database Updates

The Python consumer will:

1. Create or update the assessment record
2. Create or update the user record
3. Log the invitation details

## Monitoring

### RabbitMQ Management UI

Access the RabbitMQ management interface at: http://localhost:15672
- Username: guest
- Password: guest

### Logs

The consumer logs all activities including:
- Connection status
- Message processing
- Database updates
- Errors

## Error Handling

- Messages are automatically requeued on processing errors
- Connection failures trigger reconnection attempts
- Database errors are logged and the message is requeued

## Development

### Testing the Publisher

You can test the publisher by inviting a candidate to an assessment through the Java backend API.

### Testing the Consumer

1. Start the consumer
2. Invite a candidate through the Java backend
3. Check the consumer logs for message processing
4. Verify database updates in the Python service

## Troubleshooting

### Common Issues

1. **Connection refused**: Ensure RabbitMQ is running
2. **Queue not found**: Check that the exchange and queue are properly declared
3. **Database errors**: Verify database connection and schema

### Debug Mode

To enable debug logging, modify the logging level in `run_consumer.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
``` 