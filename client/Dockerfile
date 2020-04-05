ARG NODE_VERSION=12.16.1
FROM node:$NODE_VERSION as builder

# Build in development allow devDependencies/dependencies to be installed correctly
ENV NODE_ENV development

ARG BUILD_MODE=production
ENV BUILD_MODE $BUILD_MODE

RUN npm i npm@latest -g

# Create app directory
RUN mkdir /usr/src/app && chown -R node:node /usr/src/app
WORKDIR /usr/src/app

# the official node image provides an unprivileged user as a security best practice
# but we have to manually enable it. We put it here so npm installs dependencies as the same
# user who runs the app. 
# https://github.com/nodejs/docker-node/blob/master/docs/BestPractices.md#non-root-user
USER node

COPY . ./

# Set libary directory permissions
USER root
RUN chown -R node:node /usr/src/app
USER node

# Install app dependencies and set PATH variable
# Even in production, install devDependencies
RUN npm ci --no-optional
ENV PATH $PATH:/usr/src/app/node_modules/.bin:$PATH
RUN npm run build

# check every 30s to ensure this service returns HTTP 200
# HEALTHCHECK --interval=30s CMD node healthcheck.js

################################
## Final image to run the app ##
################################
FROM node:$NODE_VERSION

# Run app with an environment equal to the mode that it was built
ARG BUILD_MODE=production
ENV BUILD_MODE $BUILD_MODE
ENV NODE_ENV $BUILD_MODE
RUN echo "Running app in $NODE_ENV"

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app .
WORKDIR /usr/src/app
CMD ["node", "./server.js"]
