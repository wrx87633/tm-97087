FROM alpine:latest
ENV STUDENT_ID="97087"
ENTRYPOINT echo "Hello - Student ID: $STUDENT_ID"
